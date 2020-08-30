import logging
import os

from fastapi import FastAPI

from price_recommender.api.mux import api_router
from price_recommender.core import config
from price_recommender.core.events import shutdown_handler, startup_handler


def create_server() -> FastAPI:
    application = FastAPI(
        debug=config.DEBUG, title=config.PROJECT_NAME, version=config.VERSION
    )
    application.add_event_handler("startup", startup_handler(application))
    application.add_event_handler("shutdown", shutdown_handler(application))

    application.include_router(api_router, prefix=config.API_PREFIX)

    @application.get("/")
    async def health_check():
        return {"status": True}

    return application


app = create_server()
