import typing as t

from price_recommender.internal.domains.attributes import AttributesOrder
from price_recommender.internal.repository.drivers import AsyncIOMotorClient
from price_recommender.internal.repository.mongodb.common import MongoCRUD


class OrderServices(MongoCRUD):
    def __init__(self, *args):
        for arg in args:
            if not isinstance(arg, AttributesOrder):
                self.model = AttributesOrder
        self.collection = "attributes_index"
        self.idx_params = "name"
        self.change_params = "id"
        self.exchange_params = "value"
        kwargs = {
            "idx_params": self.idx_params,
            "change_params": self.change_params,
            "exchange_params": self.exchange_params,
        }
        super(OrderServices, self).__init__(
            self.model, args[1], self.collection, **kwargs
        )

    async def __filter_nan__(
        self, list_docs: t.List[t.Dict], exchange_params: str = "value"
    ):
        on_mongo_nan = [
            i[self.idx_params]
            for i in await self.get_all_docs()
            if i[exchange_params] == "nan"
        ]
        return [i for i in list_docs if i["name"] in on_mongo_nan]
