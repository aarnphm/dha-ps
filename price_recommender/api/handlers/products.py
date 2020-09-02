import time

from fastapi import APIRouter, Depends
from loguru import logger as log
from starlette.requests import Request
from starlette.responses import JSONResponse

from price_recommender.internal.domains.attributes import AttributesOrder
from price_recommender.internal.domains.products import ProductsCorpus
from price_recommender.internal.repository import processing as dataproc
from price_recommender.internal.repository.drivers import (AsyncIOMotorClient,
                                                           get_database)
from price_recommender.internal.repository.mongodb.corpus import CorpusServices
from price_recommender.internal.repository.mongodb.orders import OrderServices

products_router = APIRouter()


def get_corpus_services(db: AsyncIOMotorClient = Depends(get_database)):
    return CorpusServices(ProductsCorpus, db)


def get_order_services(db: AsyncIOMotorClient = Depends(get_database)):
    return OrderServices(AttributesOrder, db)


async def get_order_idx(
    db: AsyncIOMotorClient = Depends(get_database),
    order_services: OrderServices = Depends(get_order_services),
):
    return [i["value"] for i in await order_services.get_all_docs()]


@products_router.post("/")
async def create_corpus(
    req: Request,
    db: AsyncIOMotorClient = Depends(get_database),
    corpus_services: CorpusServices = Depends(get_corpus_services),
    order_services: OrderServices = Depends(get_order_services),
):
    """generate corpus from database"""
    content = await req.json()
    ord_body = await get_order_idx(db, order_services)

    # logic starts here
    res = dataproc.gen_corpus(body=content, ord_body=ord_body, orders_path=None)
    # return {"length": len(res), "corpus": res}
    return {"generated corpus": True}


@products_router.post("/{idx}")
async def infer_product(
    req: Request,
    idx: int,
    db: AsyncIOMotorClient = Depends(get_database),
    corpus_services: CorpusServices = Depends(get_corpus_services),
    order_services: OrderServices = Depends(get_order_services),
):
    """infer product given id"""
    content = await req.json()
    ord_body = await get_order_idx(db, order_services)
    model = req.app.state.model

    try:
        start = time.time()
        res = dataproc.gen_corpus(body=content, ord_body=ord_body, orders_path=None)[0]
        await corpus_services.insert_one_doc(res)
        products_list = await corpus_services.get_all_descriptions()
        log.debug(f"Product info: {res['description']}")
        log.debug(f"Product list: {products_list}")
        prediction = model.infer(corpus=products_list, products=res["description"])
        log.debug(f"Elapsed time: {(time.time()-start)*1000:.3f}ms")
        return JSONResponse(content=prediction)
    except Exception as exception:
        log.error(exception)
        raise exception
