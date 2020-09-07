from fastapi import APIRouter, Depends, Request

from price_recommender.internal.domains.attributes import AttributesOrder
from price_recommender.internal.repository.drivers import (AsyncIOMotorClient,
                                                           get_database)
from price_recommender.internal.repository.mongodb.orders import OrderServices

attributes_router = APIRouter()


@attributes_router.post("/")
async def update_attributes_to_mongo(
    request: Request, db: AsyncIOMotorClient = Depends(get_database)
):
    order_services = OrderServices(AttributesOrder, db)
    attrs = await request.json()
    return await order_services.update_many_docs(attrs)
