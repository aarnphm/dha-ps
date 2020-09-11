import logging as log
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


async def get_corpus_order_corpus(
    req: Request,
    idx: str = "many",
    order_services: OrderServices = Depends(get_order_services),
):
    assert idx in ["many", "one"], f"supported `many` and `one` tags, got {idx} instead"
    order = [i["value"] for i in await order_services.get_all_docs()]
    body = await req.json()
    res = dataproc.gen_corpus(body=body, ord_body=order)
    return res if idx == "many" else res[0]


@products_router.post("/")
async def create_corpus(
    req: Request,
    corpus_services: CorpusServices = Depends(get_corpus_services),
    order_services: OrderServices = Depends(get_order_services),
):
    """generate corpus from database"""
    res = await get_corpus_order_corpus(req, order_services=order_services)
    try:
        # return {"length": len(res), "corpus": res}
        await corpus_services.insert_many_descriptions(res)
        return {"generated corpus": True}
    except isinstance(res, str):
        return JSONResponse(content={"info": res}, status_code=404)
    except Exception as e:
        log.error(e)
        return JSONResponse(
            content={"internal error": True, "exception": e}, status_code=500
        )


@products_router.post("/{idx}")
async def infer_product(
    req: Request,
    idx: int,
    corpus_services: CorpusServices = Depends(get_corpus_services),
    order_services: OrderServices = Depends(get_order_services),
):
    """infer product given id"""
    model = req.app.state.model
    products_list = await corpus_services.get_all_descriptions()
    res = await get_corpus_order_corpus(req, idx="one", order_services=order_services)
    try:
        start = time.time()
        await corpus_services.insert_one_doc(res)
        prediction = model.infer(corpus=products_list, products=res)
        log.debug(f"Elapsed time: {(time.time()-start)*1000:.3f}ms")
        return JSONResponse(content=prediction)
    except Exception as exception:
        log.error(exception)
        return JSONResponse(content={"error ids": idx}, status_code=404)
