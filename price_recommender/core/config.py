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

DEBUG: bool = os.getenv("DEBUG")
SECRET_KEY: Secret = os.getenv("SECRET_KEY")
PROJECT_NAME: str = os.getenv("PROJECT_NAME")
ALLOWED_HOST: t.List[str] = str(os.getenv("ALLOWED_HOST")).split(",")
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

MONGO_URI: str = str(os.getenv("MONGO_URI"))
