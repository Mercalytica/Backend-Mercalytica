from motor.motor_asyncio import AsyncIOMotorClient

class MongoConnector:
    def __init__(self, uri:str, db_name:str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def find_all(self, collection_name):
        cursor = self.db[collection_name].find()
        return await cursor.to_list(length=None)

    async def aggregate(self, collection_name, pipeline):
        cursor = self.db[collection_name].aggregate(pipeline)
        return await cursor.to_list(length=None)

    async def count(self, collection_name):
        return await self.db[collection_name].count_documents({})