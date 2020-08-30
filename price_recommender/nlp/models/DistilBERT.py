"""implement huggingface's DistilBERT model at fine-tuning"""
import json
import logging
import os
from typing import Dict, List, Optional

import numpy as np
from torch import Tensor, nn
from transformers import DistilBertModel, DistilBertTokenizer


class DistilBERT(nn.Module):
    """DistilBERT to generate token embedding
    each token is mapped to an output vector from DistilBERT"""

    def __init__(
        self,
        model_name: str,
        max_seq_length: int = 128,
        do_lower_case: Optional[bool] = None,
        model_args: Dict = {},
        tokenizer_args: Dict = {},
    ):
        super(DistilBERT, self).__init__()
        self.config_keys = ["max_seq_length", "do_lower_case"]
        self.do_lower_case = do_lower_case

        if max_seq_length > 510:
            logging.warning(
                "BERT only allows max_seq_length of 510 (512 with special token). set to 510"
            )
            max_seq_length = 510
        self.max_seq_length = max_seq_length

        if self.do_lower_case is not None:
            tokenizer_args["do_lower_case"] = do_lower_case

        self.bert = DistilBertModel.from_pretrained(model_name, **model_args)
        self.tokenizer = DistilBertTokenizer.from_pretrained(
            model_name, **tokenizer_args
        )

    def forward(self, features):
        """return token_embeddings, cls_token"""
        # DistiBERT doesn't use token_type_id
        output_states = self.bert(**features)
        output_tokens = output_states[0]
        cls_tokens = output_tokens[:, 0, :]  # [CLS] is the first token
        features.update(
            {
                "token_embeddings": output_tokens,
                "cls_token_embeddings": cls_tokens,
                "attention_mask": features["attention_mask"],
            }
        )

        if len(output_states) > 1:
            features.update({"all_layer_embeddings": output_states[1]})

        return features

    def get_word_embedding_dimension(self) -> int:
        """return embedding dimension of BERT"""
        return self.bert.config.hidden_size

    def tokenize(self, text: str) -> List[int]:
        """Tokenizes a text and maps tokens to token-ids"""
        return self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(text))

    def get_sentence_features(self, tokens: List[int], pad_seq_length: int):
        """convert tokenized sentenced in its embedding ids, segment ids and mask

        :param tokens: tokenized sentence
        :param pad_seq_length: maximal length of the sequence. Cannot be greater than self.sentence_transformer_config.max_seq_length
        :return: embedding ids, segment ids and mask for given sentence"""
        pad_seq_length = min(pad_seq_length, self.max_seq_length) + 2  # special tokens
        return self.tokenizer.prepare_for_model(
            tokens,
            max_length=pad_seq_length,
            pad_to_max_length=True,
            return_tensors="pt",
            truncation=True,
        )

    def get_config_dict(self):
        """return model config"""
        return {key: self.__dict__[key] for key in self.config_keys}

    def save(self, output_path: str):
        """save model to a sub-folder"""
        self.bert.save_pretrained(output_path)
        self.tokenizer.save_pretrained(output_path)
        with open(
            os.path.join(output_path, "sentence_distilbert_config.json"), "w"
        ) as out:
            json.dump(self.get_config_dict(), out, indent=2)

    @staticmethod
    def load(input_path: str):
        with open(os.path.join(input_path, "sentence_distilbert_config.json")) as fin:
            config = json.load(fin)
        return DistilBERT(model_name=input_path, **config)
