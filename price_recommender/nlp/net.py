"""main modules responsible for inference, check out sentence-transformers repo here: https://github.com/UKPLab/sentence-transformers """
import json
import logging
import math
import os
import queue
import time
from collections import OrderedDict
from typing import Dict, Iterable, List, Tuple, Union

import numpy as np
import torch
import torch.multiprocessing as mp
from loguru import logger as log
from torch import Tensor, nn
from torch.utils.data import DataLoader, Dataset

try:
    from price_recommender.nlp.helpers import (
        MODELS,
        get_default_cache_path,
        import_from_string,
        pytorch_cdist,
    )
except ImportError:
    from helpers import (
        MODELS,
        get_default_cache_path,
        import_from_string,
        pytorch_cdist,
    )

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


class SentenceTransformer(nn.Sequential):
    """
    SentenceTransformer : a siamsese NN composed from BERT (DistilBERT)
    """

    def __init__(
        self,
        model_name_or_path: str = MODELS,
        modules: Iterable[nn.Module] = None,
        device: str = None,
        API=True,
    ):
        self.model_name = MODELS
        if modules is not None and not isinstance(modules, OrderedDict):
            modules = OrderedDict(
                [(str(idx), module) for idx, module in enumerate(modules)]
            )

        assert (
            model_name_or_path is not None and model_name_or_path != ""
        ), "You forgot to include distilBERT =("
        log.info("Loading pretrained: {}".format(model_name_or_path))

        if not API:
            model_path = get_default_cache_path()
        else:
            model_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), MODELS
            )
        log.info(
            f"Load model from {'.'.join(model_path.split('/')[-3:])}, Mode: {'API' if API else 'local'}"
        )

        # Load from disk
        with open(os.path.join(model_path, "modules.json")) as fIn:
            contained_modules = json.load(fIn)

        modules = OrderedDict()
        for module_config in contained_modules:
            module_class = import_from_string(module_config["type"], API=API)
            module = module_class.load(os.path.join(model_path, module_config["path"]))
            modules[module_config["name"]] = module

        super().__init__(modules)
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            log.info("Use {} for running PyTorch".format(device))

        self._target_device = torch.device(device)

    def infer(
        self,
        corpus: List[str],
        products: Union[str, List[str]],
        cluster: int = 5,
        verbose=False,
    ) -> Dict[str, str]:
        """returns products that is similar to given product"""
        self.eval()
        start = time.time()
        closest = {}
        if isinstance(products, str):
            products = [products]
        corpus_embeddings = self.encode(corpus, convert_to_tensor=True)
        for product in products:
            product_embeddings = self.encode(product, convert_to_tensor=True)
            emb_time = time.time() - start

            cos_scores = pytorch_cdist(product_embeddings, corpus_embeddings)[0]
            cos_scores = cos_scores.cpu().numpy()
            res = np.argpartition(-cos_scores, range(cluster))[0:cluster]
            if verbose:
                log.info("embedding took : {:.4f}s".format(emb_time))
                log.info(f"\n\n{'='*150}\n\n")
                log.info("Input: {}".format(product))
                log.info("Clusters of {} similar products:".format(cluster))
            for idx in res[0:cluster]:
                closest[cos_scores[idx]] = corpus[idx].strip()
                if verbose:
                    log.info(
                        f"Desc: {corpus[idx].strip()} | Scores: {cos_scores[idx]:.4f}"
                    )

        return closest

    def encode(
        self,
        sentences: Union[str, List[str], List[int]],
        batch_size: int = 32,
        output_value: str = "sentence_embedding",
        convert_to_numpy: bool = True,
        convert_to_tensor: bool = False,
        is_pretokenized: bool = False,
        device: str = None,
        num_workers: int = 0,
    ) -> Union[List[Tensor], np.ndarray, Tensor]:
        """
        Computes sentence embeddings
        :param sentences: the sentences to embed
        :param batch_size: the batch size used for the computation
        :param output_value:  Default sentence_embedding, to get sentence embeddings. Can be set to token_embeddings to get wordpiece token embeddings.
        :param convert_to_numpy: If true, the output is a list of numpy vectors. Else, it is a list of pytorch tensors.
        :param convert_to_tensor: If true, you get one large tensor as return. Overwrites any setting from conver_to_numy
        :param is_pretokenized: If is_pretokenized=True, sentences must be a list of integers, containing the tokenized sentences with each token convert to the respective int.
        :param device: Which torch.device to use for the computation
        :param num_workers: Number of background-workers to tokenize data. Set to positive number to increase tokenization speed
        :return:
           By default, a list of tensors is returned. If convert_to_tensor, a stacked tensor is returned. If convert_to_numpy, a numpy matrix is returned.
        """
        self.eval()

        input_was_string = False
        if isinstance(sentences, str):
            sentences = [sentences]
            input_was_string = True

        if device is None:
            device = self._target_device

        self.to(device)

        all_embeddings = []
        length_sorted_idx = np.argsort([len(sen) for sen in sentences])
        sentences_sorted = [sentences[idx] for idx in length_sorted_idx]
        inp_dataset = EncodeDataset(
            sentences_sorted, model=self, is_tokenized=is_pretokenized
        )
        inp_dataloader = DataLoader(
            inp_dataset,
            batch_size=batch_size,
            collate_fn=self.smart_batching_collate_text_only,
            num_workers=num_workers,
            shuffle=False,
        )

        iterator = inp_dataloader

        for features in iterator:
            for feature_name in features:
                features[feature_name] = features[feature_name].to(device)

            with torch.no_grad():
                out_features = self.forward(features)
                embeddings = out_features[output_value]

                if output_value == "token_embeddings":
                    # Set token embeddings to 0 for padding tokens
                    input_mask = out_features["attention_mask"]
                    input_mask_expanded = (
                        input_mask.unsqueeze(-1).expand(embeddings.size()).float()
                    )
                    embeddings = embeddings * input_mask_expanded

                all_embeddings.extend(embeddings)

        all_embeddings = [all_embeddings[idx] for idx in np.argsort(length_sorted_idx)]

        if convert_to_tensor:
            all_embeddings = torch.stack(all_embeddings)
        elif convert_to_numpy:
            all_embeddings = np.asarray(
                [emb.cpu().detach().numpy() for emb in all_embeddings]
            )

        if input_was_string:
            all_embeddings = all_embeddings[0]

        return all_embeddings

    def start_multi_process_pool(
        self, target_devices: List[str] = None, encode_batch_size: int = 32
    ):
        """
        Starts multi process to process the encode with several, independent  process.
        This methos is recommend if you want to encode on multiple GPUs. It is advised
        to start only one process per GPU. This method works together with encode_multi_process
        :param target_devices: PyTorch target devices, e.g. cuda:0, cuda:1... If None, all available CUDA devices will be used
        :param encode_batch_size: Batch size for each process when calling encode
        :return: Returns a dict with the target processes, an input queue and and output queue.
        """
        if target_devices is None:
            if torch.cuda.is_available():
                target_devices = [
                    "cuda:{}".format(i) for i in range(torch.cuda.device_count())
                ]
            else:
                logging.info("CUDA is not available. Start 4 CPU worker")
                target_devices = ["cpu"] * 4

        logging.info(
            "Start multi-process pool on devices: {}".format(
                ", ".join(map(str, target_devices))
            )
        )

        ctx = mp.get_context("spawn")
        input_queue = ctx.Queue()
        output_queue = ctx.Queue()
        processes = []

        for cuda_id in target_devices:
            p = ctx.Process(
                target=SentenceTransformer._encode_multi_process_worker,
                args=(cuda_id, self, input_queue, output_queue, encode_batch_size),
                daemon=True,
            )
            p.start()
            processes.append(p)

        return {"input": input_queue, "output": output_queue, "processes": processes}

    @staticmethod
    def stop_multi_process_pool(pool):
        """
        Stops all processes started with start_multi_process_pool
        """
        for p in pool["processes"]:
            p.terminate()

        for p in pool["processes"]:
            p.join()
            p.close()

        pool["input"].close()
        pool["output"].close()

    def encode_multi_process(
        self,
        sentences: List[str],
        pool: Dict[str, object],
        is_pretokenized: bool = False,
    ):
        """
        This method allows to run encode() on multiple GPUs. The sentences are chunked into smaller packages
        and sent to individual processes, which encode these on the different GPUs. This method is only suitable
        for encoding large sets of sentences
        :param sentences: List of sentences
        :param pool: A pool of workers started with SentenceTransformer.start_multi_process_pool
        :param is_pretokenized: If true, no tokenization will be applied. It is expected that the input sentences are list of ints.
        :return: Numpy matrix with all embeddings
        """

        chunk_size = min(math.ceil(len(sentences) / len(pool["processes"]) / 10), 5000)
        logging.info("Chunk data into packages of size {}".format(chunk_size))

        if is_pretokenized:
            sentences_tokenized = sentences
        else:
            sentences_tokenized = map(self.tokenize, sentences)

        input_queue = pool["input"]
        num_chunks = 0
        chunk = []

        for sentence in sentences_tokenized:
            chunk.append(sentence)
            if len(chunk) >= chunk_size:
                input_queue.put([num_chunks, chunk])
                num_chunks += 1
                chunk = []

        if len(chunk) > 0:
            input_queue.put([num_chunks, chunk])
            num_chunks += 1

        output_queue = pool["output"]
        results_list = sorted(
            [output_queue.get() for _ in range(num_chunks)], key=lambda x: x[0]
        )
        embeddings = np.concatenate([result[1] for result in results_list])
        return embeddings

    @staticmethod
    def _encode_multi_process_worker(
        target_device: str, model, input_queue, results_queue, encode_batch_size
    ):
        """
        Internal working process to encode sentences in multi-process setup
        """
        while True:
            try:
                id, sentences = input_queue.get()
                embeddings = model.encode(
                    sentences,
                    device=target_device,
                    is_pretokenized=True,
                    convert_to_numpy=True,
                    batch_size=encode_batch_size,
                )
                results_queue.put([id, embeddings])
            except queue.Empty:
                break

    def get_max_seq_length(self):
        """
        Returns the maximal sequence length for input the model accepts. Longer inputs will be truncated
        """
        if hasattr(self._first_module(), "max_seq_length"):
            return self._first_module().max_seq_length

        return None

    def tokenize(self, text: str):
        """
        Tokenizes the text
        """
        return self._first_module().tokenize(text)

    def get_sentence_features(self, *features):
        return self._first_module().get_sentence_features(*features)

    def get_sentence_embedding_dimension(self):
        return self._last_module().get_sentence_embedding_dimension()

    def _first_module(self):
        """Returns the first module of this sequential embedder"""
        return self._modules[next(iter(self._modules))]

    def _last_module(self):
        """Returns the last module of this sequential embedder"""
        return self._modules[next(reversed(self._modules))]

    def smart_batching_collate_text_only(self, batch):
        """
        Transforms a batch from a SmartBatchingDataset to a batch of tensors for the model
        :param batch:
            a batch from a SmartBatchingDataset
        :return:
            a batch of tensors for the model
        """

        max_seq_len = max([len(text) for text in batch])
        feature_lists = {}

        for text in batch:
            sentence_features = self.get_sentence_features(text, max_seq_len)
            for feature_name in sentence_features:
                if feature_name not in feature_lists:
                    feature_lists[feature_name] = []

                feature_lists[feature_name].append(sentence_features[feature_name])

        for feature_name in feature_lists:
            feature_lists[feature_name] = torch.cat(feature_lists[feature_name])

        return feature_lists

    @property
    def device(self) -> torch.device:
        """
        Get torch.device from module, assuming that the whole module has one device.
        """
        try:
            return next(self.parameters()).device
        except StopIteration:
            # For nn.DataParallel compatibility in PyTorch 1.5

            def find_tensor_attributes(module: nn.Module) -> List[Tuple[str, Tensor]]:
                tuples = [
                    (k, v) for k, v in module.__dict__.items() if torch.is_tensor(v)
                ]
                return tuples

            gen = self._named_members(get_members_fn=find_tensor_attributes)
            first_tuple = next(gen)
            return first_tuple[1].device

    @property
    def tokenizer(self):
        """
        Property to get the tokenizer that is used by this model
        """
        return self._first_module().tokenizer

    @tokenizer.setter
    def tokenizer(self, value):
        """
        Property to set the tokenizer that is should used by this model
        """
        self._first_module().tokenizer = value

    @property
    def max_seq_length(self):
        """
        Property to get the maximal input sequence length for the model. Longer inputs will be truncated.
        """
        return self._first_module().max_seq_length

    @max_seq_length.setter
    def max_seq_length(self, value):
        """
        Property to set the maximal input sequence length for the model. Longer inputs will be truncated.
        """
        self._first_module().max_seq_length = value


class EncodeDataset(Dataset):
    def __init__(
        self,
        sentences: Union[List[str], List[int]],
        model: SentenceTransformer,
        is_tokenized: bool = True,
    ):
        """
        EncodeDataset is used by SentenceTransformer.encode method. It just stores
        the input texts and returns a tokenized version of it.
        """
        self.model = model
        self.sentences = sentences
        self.is_tokenized = is_tokenized

    def __getitem__(self, item):
        return (
            self.sentences[item]
            if self.is_tokenized
            else self.model.tokenize(self.sentences[item])
        )

    def __len__(self):
        return len(self.sentences)


if __name__ == "__main__":
    m = SentenceTransformer(device="cpu", API=False)
    test_corpus = [
        "Leanna Ladies (M-L)",
        "Paige V (S-XL)",
        "SAM'S (Pant) (S-L)",
        "Vải chống thấm Tuytsi",
        "Áo polo Nam (ALL)",
        "SAM'S (Body) (S-L)",
        "SAM'S (Polo) (S-L)",
        "crew neck fitted rib tee (ALL)",
        "A1 (M-L) Denim Da lộn",
        "Áo sơ mi Carter (ALL)",
        "Áo sơ mi Carter (M-L)",
        "Test (ALL)",
        "Ao Bell SS 01  (S-M)",
    ]
    test_queries = "Leanna Ladies (M-L)"
    _ = m.infer(corpus=test_corpus, products=test_queries, verbose=True)
