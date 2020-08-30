import logging
import os
import typing as t

from dotenv import find_dotenv, load_dotenv
from starlette.datastructures import Secret

load_dotenv(find_dotenv())
API_PREFIX = "/api/v1"

VERSION = "0.0.1-dev"

IDX_COLUMN: str = "product_id"
SIZE_VAL: int = 30
COLOUR_VAL: int = 4
SIZE: t.Tuple[str] = ("2XS", "XS", "S", "M", "L", "XL", "2XL", "ALL")

LOGGING_LEVEL = logging.DEBUG
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

MONGO_URI: str = str(os.getenv("MONGO_URI"))
