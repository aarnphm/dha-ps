import os
from typing import Callable, List

import numpy as np
from fastapi import FastAPI
from loguru import logger as log
# from price_recommender.nlp.net import SentenceTransformer
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

    def infer(self, corpus: List[str], products: str, cluster: int = 5):
        closest = {}
        corpus_embedding = self.model.encode(corpus, convert_to_tensor=True)
        query_embedding = self.model.encode(products, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embedding)[0]
        cos_scores = cos_scores.cpu()

        top = np.argpartition(-cos_scores, range(cluster))[0:cluster]
        for idx in top[0:cluster]:
            closest[str(cos_scores[idx])] = corpus[idx].strip()
        return closest


def __startup_model__(app: FastAPI) -> None:
    nlp = Model()
    app.state.model = nlp


def __shutdown_model__(app: FastAPI) -> None:
    app.state.model = None


def startup_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        connect()
        log.info("Running inference server...")
        __startup_model__(app)

    return start_app


def shutdown_handler(app: FastAPI) -> Callable:
    @log.catch
    async def close_app() -> None:
        disconnect()
        log.info("Shuting down...")
        __shutdown_model__(app)

    return close_app
