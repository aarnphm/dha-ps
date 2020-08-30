import json
import multiprocessing
import os
import time
from collections import OrderedDict
from multiprocessing import Pool, cpu_count
from typing import Dict, Iterable, List, Tuple, Union

import numpy as np
import torch
from loguru import logger as log
from torch import Tensor, nn

from price_recommender.nlp.helpers import *

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


class SentenceTransformer(nn.Sequential):
    """
    SentenceTransformer : a siamsese NN composed from BERT (DistilBERT)
    """

    # pylint: disable=too-many-locals,invalid-name
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
        self, corpus: List[str], products: str, cluster: int = 5, verbose=False
    ) -> Dict[str, str]:
        """returns products that is similar to given product"""
        self.eval()
        start = time.time()
        closest = {}
        corpus_embeddings = self.encode(corpus, to_tensor=True)
        product_embeddings = self.encode(products, to_tensor=True)
        emb_time = time.time() - start

        cos_scores = pytorch_cdist(product_embeddings, corpus_embeddings)[0]
        cos_scores = cos_scores.to("cpu").numpy()
        res = np.argpartition(-cos_scores, range(cluster))[0:cluster]
        for idx in res[0 : cluster + 2]:
            closest[str(cos_scores[idx])] = corpus[idx].strip()
        if verbose:
            log.info("embedding took : {:.4f}s".format(emb_time))
            log.info("Input: {}".format(products))
            log.info("Clusters of {} similar products:".format(cluster))
            for k, v in closest.items():
                log.info("Desc: {} | Scores: {:.4f}".format(v, float(k)))

        return closest

    def encode(
        self,
        sentences: Union[str, List[str], List[int]],
        batch_size: int = 8,
        output_value: str = "sentence_embedding",
        to_numpy: bool = True,
        to_tensor: bool = False,
        is_pretokenized: bool = False,
    ) -> Union[List[Tensor], np.ndarray, Tensor]:
        """
        Computes sentence embedding

        :param sentence: sentences to be embedded, can be str, list(str) or list of tokenized string
        :param batch_size: batch size used for computing
        :param output_value: default is `sentence_embedding` to get sentence embedding.
         Can set to `token_embedding` to get wordpiece token embedding
        :param to_numpy: convert result to a list of numpy vectors, else PyTorch vectors
        :param to_tensor: if true, get one large tensor, overwrite `to_numpy`
        :param is_pretokenized: if true, sentences must be a list of int, containing tokenized
         sentences with each token convert to respective int
        """
        self.eval()
        if isinstance(sentences, str):
            sentences = [sentences]
        all_embeddings = []
        if is_pretokenized:
            sentences_tokenized = sentences
        else:
            if (
                not self.parallel_tokenization
                or len(sentences) < self.parallel_tokenization_chunksize
            ):
                sentences_tokenized = [self.tokenize(sen) for sen in sentences]
            else:
                log.info(
                    "Multiprocess tokenization with {} workers".format(
                        self.parallel_tokenization_processes
                    )
                )
                self.to("cpu")
                with Pool(self.parallel_tokenization_processes) as pool:
                    sentences_tokenized = list(
                        pool.imap(
                            self.tokenize,
                            sentences,
                            chunksize=self.parallel_tokenization_chunksize,
                        )
                    )
        self.to(self._target_device)
        length_sorted_idx = np.argsort([len(sen) for sen in sentences])

        for batch_idx in range(0, len(sentences), batch_size):
            batch_tokens = []

            batch_start = batch_idx
            batch_end = min(batch_start + batch_size, len(sentences))

            longest_seq = 0

            for idx in length_sorted_idx[batch_start:batch_end]:
                tokens = sentences_tokenized[idx]
                longest_seq = max(longest_seq, len(tokens))
                batch_tokens.append(tokens)

            features = {}
            for text in batch_tokens:
                sentence_features = self.get_sentence_features(text, longest_seq)

                for feature_name in sentence_features:
                    if feature_name not in features:
                        features[feature_name] = []
                    features[feature_name].append(sentence_features[feature_name])

            for feature_name in features:
                features[feature_name] = torch.cat(features[feature_name]).to(
                    self._target_device
                )

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

        reverting_order = np.argsort(length_sorted_idx)
        all_embeddings = [all_embeddings[idx] for idx in reverting_order]

        if to_tensor:
            all_embeddings = torch.stack(all_embeddings)
        elif to_numpy:
            all_embeddings = np.asarray(
                [emb.cpu().detach().numpy() for emb in all_embeddings]
            )

        return all_embeddings

    def save(self, path):
        if path is None:
            return
        log.info("Save model to {}".format(path))
        contained_modules = []
        for idx, name in enumerate(self._modules):
            module = self._modules[name]
            model_path = os.path.join(path, str(idx) + "_" + type(module).__name__)
            os.makedirs(model_path, exist_ok=True)
            module.save(model_path)
            contained_modules.append(
                {
                    "idx": idx,
                    "name": name,
                    "path": os.path.basename(model_path),
                    "type": type(module).__module__,
                }
            )
        with open(os.path.join(path, "modules.json"), "w") as out:
            json.dump(contained_modules, out, indent=2)

    @property
    def device(self) -> torch.device:
        """return torch.device from module"""
        try:
            return next(self.parameters()).device
        except StopIteration:
            # nn.DataParallel in PyTorch 1.5
            def find_tensor_attributes(module: nn.Module) -> List[Tuple[str, Tensor]]:
                return [
                    (k, v) for k, v in module.__dict__.items() if torch.is_tensor(v)
                ]

            gen = self._named_members(get_members_fn=find_tensor_attributes)
            first_tuple = next(gen)
            return first_tuple[1].device

    @property
    def tokenizer(self):
        """property to get tokenized used by this model"""
        return self._first_module().tokenizer

    @tokenizer.setter
    def tokenizer(self, value):
        """property to set the tokenizer that is used by this model"""
        self._first_module().tokenizer = value

    # property function to implements from transformers
    def tokenize(self, text):
        return self._first_module().tokenize(text)

    def get_sentence_features(self, *features):
        return self._first_module().get_sentence_features(*features)

    def get_sentence_embedding_dimension(self):
        return self._last_module().get_sentence_embedding_dimension()

    def _first_module(self):
        return self._modules[next(iter(self._modules))]

    def _last_module(self):
        return self._modules[next(reversed(self._modules))]
