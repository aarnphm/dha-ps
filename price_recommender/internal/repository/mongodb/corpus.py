import typing as t

from price_recommender.internal.domains.products import ProductsCorpus
from price_recommender.internal.repository.mongodb.common import MongoCRUD


class CorpusServices(MongoCRUD):
    def __init__(self, *args):
        if not isinstance(args[0], ProductsCorpus):
            self.model = ProductsCorpus
        self.collection = "corpus"
        self.idx_params = "product_id"
        self.change_params = "description"
        kwargs = {"idx_params": self.idx_params, "change_params": self.change_params}
        super(CorpusServices, self).__init__(
            self.model, args[1], self.collection, **kwargs
        )

    async def __filter_nan__(self, list_docs: t.List[t.Dict]) -> t.List[t.Dict]:
        ids = await self.get_all_descriptions(ids=True)
        return [it for it in list_docs if str(it[self.idx_params]) not in ids]

    async def insert_many_descriptions(self, list_docs: t.List[t.Dict]):
        filtered = await self.__filter_nan__(list_docs)
        await super().insert_many_docs(filtered)

    async def get_all_descriptions(self, ids=False):
        docs = await super().get_all_docs()
        return [str(d[self.idx_params]) for d in docs] if ids else [d for d in docs]
