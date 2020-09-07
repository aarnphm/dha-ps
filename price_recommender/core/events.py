import os
from typing import Callable, Dict, List

import numpy as np
from fastapi import FastAPI
from loguru import logger as log
from sentence_transformers import SentenceTransformer, util

from price_recommender.internal.repository.utils import connect, disconnect


class Model:
    def __init__(
        self,
        model: str = "/app/price_recommender/distilbert-base-nli-stsb-mean-tokens",
    ):
        if not os.path.exists(model):
            model = "distilbert-base-nli-stsb-mean-tokens"
        self.model = SentenceTransformer(model)

    def infer(self, corpus: List[Dict], products: Dict, cluster: int = 5):
        closest = {}
        res = {i["product_id"]: i["description"] for i in corpus}
        corpus_embedding = self.model.encode(list(res.values()), convert_to_tensor=True)
        query_embedding = self.model.encode(
            products["description"], convert_to_tensor=True
        )
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embedding)[0]
        cos_scores = cos_scores.cpu()

        top = np.argpartition(-cos_scores, range(cluster))[0:cluster]
        for idx in top[1 : cluster + 2]:
            closest[str(cos_scores[idx])] = list(res.values())[idx].strip()
        res_idx = {
            k: list(res.keys())[list(res.values()).index(v)] for k, v in closest.items()
        }
        return res_idx


def __startup_model__(app: FastAPI) -> None:
    nlp = Model()
    app.state.model = nlp


def __shutdown_model__(app: FastAPI) -> None:
    app.state.model = None


def startup_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        connect()
        __startup_model__(app)

    return start_app


def shutdown_handler(app: FastAPI) -> Callable:
    @log.catch
    async def close_app() -> None:
        disconnect()
        __shutdown_model__(app)

    return close_app
