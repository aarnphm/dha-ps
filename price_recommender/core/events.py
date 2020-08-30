from typing import Callable

from fastapi import FastAPI
from loguru import logger as log

from price_recommender.internal.repository.utils import connect, disconnect
from price_recommender.nlp.net import SentenceTransformer


def __startup_model__(app: FastAPI) -> None:
    nlp = SentenceTransformer()
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
