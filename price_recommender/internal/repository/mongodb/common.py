import typing as t
from abc import ABC, abstractmethod

from loguru import logger as log
from pydantic import BaseModel

from price_recommender.internal.repository.drivers import AsyncIOMotorClient


class Base(ABC):
    @abstractmethod
    async def __filter_nan__(self):
        pass


class MongoCRUD(Base):
    def __init__(
        self,
        model: BaseModel,
        conn: AsyncIOMotorClient,
        collection,
        database: str = "backend",
        **kwargs,
    ):
        self.model = model
        self.conn = conn
        self.collection = collection
        self.database = database

        self.__get_default_keys__()
        self.__get_trx__()

        self.idx_params = kwargs.get("idx_params")
        self.change_params = kwargs.get("change_params")
        self.exchange_params = kwargs.get("exchange_params")

    def __get_trx__(self):
        self.trx = self.conn[self.database][self.collection]

    def __get_default_keys__(self):
        self.default_keys = self.model.__field_defaults__.keys()

    async def __filter_nan__(self, list_docs: t.List[t.Dict]):
        return list_docs

    def __uv__(self, obj: BaseModel, new_val: t.Union[str, int]):
        obj = obj.dict()
        obj[self.exchange_params] = new_val
        return self.model(**obj)

    def __uvdoc__(self, doc: t.Dict) -> BaseModel:
        # update value of one dict into model
        res = {}
        for key in self.default_keys:
            res[key] = doc[key]
        return self.model(**res)

    async def insert_one_doc(self, doc: t.Dict) -> t.Dict:
        processed = self.__uvdoc__(doc)
        if await self.get_one_doc_by(doc[self.idx_params]) is None:
            await self.trx.insert_one(processed.dict())
            return {"inserted": True}
        return {"inserted": False}

    async def insert_many_docs(self, list_docs: t.List[t.Dict]):
        return await self.trx.insert_many(list_docs) if len(list_docs) > 0 else None

    async def update_one_doc(self, idx_val: str, new_val: int) -> t.Dict:
        obj = await self.get_one_doc_by(idx_val)
        if obj is not None:
            targ = self.__uv__(obj, new_val)
            log.info(targ)
            await self.trx.update_one({self.idx_params: idx_val}, {"$set": targ.dict()})
            return {"updated": True}
        return {"updated": False}

    async def update_many_docs(self, list_docs: t.List[t.Dict]) -> t.Dict:
        for it in list_docs:
            ops = await self.update_one_doc(it[self.idx_params], it[self.change_params])
            if not ops["updated"]:
                log.info(f"{it[self.idx_params]} doesn't exists in DB, skipping...")
                continue
        return {"updated many": True}

    async def get_one_doc_by(self, idx_val: str):
        res = await self.trx.find_one({self.idx_params: idx_val})
        return self.model(**res) if res else None

    async def get_all_docs(self) -> t.List:
        res = []
        async for doc in self.trx.find():
            res.append(self.model(**doc).dict())
        return res
