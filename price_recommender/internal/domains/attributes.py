import typing as t

from bson.objectid import ObjectId

from price_recommender.internal.domains.common import Repository


class AttributesRepository(Repository):
    id: int
    name: str
    isproduct: bool
    ismaterial: bool
    issewingtrims: bool
    ispackingtrims: bool


class AttributesOrder(Repository):
    _id: ObjectId = None
    idx: int = ""
    name: str = ""
    value: t.Union[int, str] = ""
