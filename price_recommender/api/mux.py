from fastapi.routing import APIRouter

from price_recommender.api.handlers.attributes import attributes_router
from price_recommender.api.handlers.products import products_router

api_router = APIRouter()
api_router.include_router(products_router, tags=["products"], prefix="/products")
api_router.include_router(attributes_router, tags=["attributes"], prefix="/attributes")
