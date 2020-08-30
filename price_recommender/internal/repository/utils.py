import subprocess

from loguru import logger as log
from motor.motor_asyncio import AsyncIOMotorClient

from price_recommender.core import config
from price_recommender.internal.repository.drivers import db


def connect() -> None:
    db.client = AsyncIOMotorClient(config.MONGO_URI)
    log.info("Connected to Mongo via URI.")


def disconnect():
    db.client.close()
    log.info("Connection to Mongo closed.")
