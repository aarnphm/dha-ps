from bson.objectid import ObjectId

from price_recommender.internal.domains.common import Repository


class ProductsRepository(Repository):
    product_id: int = None
    product_name: str = None
    attribute_value_id: int = None
    attribute_value_name: str = None
    attribute_id: int = None
    atribute_name: str = None


class ProductsCorpus(Repository):
    _id: ObjectId = None
    description: str = ""
    product_id: int = ""
