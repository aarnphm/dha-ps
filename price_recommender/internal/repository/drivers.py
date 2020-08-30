from motor.motor_asyncio import AsyncIOMotorClient


class MongoDriver:
    client: AsyncIOMotorClient = None


db = MongoDriver()


async def get_database() -> AsyncIOMotorClient:
    return db.client
