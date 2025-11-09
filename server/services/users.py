from datetime import datetime


class UsersServicer:
    def __init__(self, connector):
        self.connector = connector

    async def count_by_type(self):
        pipeline = [{ "$group": { "_id": "$tipo", "count": { "$sum": 1 } } }]
        result = await self.connector.aggregate("users", pipeline)
        print( "Result in service count_by_type:", result )
        return result

    async def total_users(self):
        result =  await self.connector.count("users")
        print( "Result in service total_users :", result )
        return result

    async def users_by_location(self):
        pipeline = [{ "$group": { "_id": "$ubicacion", "count": { "$sum": 1 } } }]
        result = await self.connector.aggregate("users", pipeline)
        print( "Result in service users_by_location :", result )
        return result
    
    async def users_by_companies(self):
        pipeline = [{ "$group": { "_id": "$empresa", "count": { "$sum": 1 } } }]
        result = await self.connector.aggregate("users", pipeline)
        print( "Result in service users_by_location :", result )
        return result
    
    async def registered_after(self, year: int):
        fecha = datetime(year, 1, 1)
        query = { "fecha_registro": { "$gt": fecha } }
        result = await self.connector.db["users"].count_documents(query)
        print("Result in service registered_after:", result)
        return result

    async def last_purchase_in_year(self, year: int):
        inicio = datetime(year, 1, 1)
        fin = datetime(year + 1, 1, 1)
        query = { "ultima_compra": { "$gte": inicio, "$lt": fin } }
        result = await self.connector.db["users"].count_documents(query)
        print("Result in service last_purchase_in_year:", result)
        return result

    async def buyers_in_location(self, location: str):
        query = {
            "tipo": { "$regex": "^comprador$", "$options": "i" },
            "ubicacion": { "$regex": location, "$options": "i" }
        }
        result = await self.connector.db["users"].count_documents(query)
        print("Result in service buyers_in_location:", result)
        return result
    
    async def registered_in_company_year(self, empresa: str, year: int):
        inicio = datetime(year, 1, 1)
        fin = datetime(year + 1, 1, 1)
        query = {
            "empresa": { "$regex": empresa, "$options": "i" },
            "fecha_registro": { "$gte": inicio, "$lt": fin }
        }
        result = await self.connector.db["users"].count_documents(query)
        print("Result in service registered_in_company_year:", result)
        return result

    async def latest_registered(self, limit: int = 10):
        cursor = self.connector.db["users"].find().sort("fecha_registro", -1).limit(limit)
        result = await cursor.to_list(length=None)
        print("Result in service latest_registered:", result)
        return result

    async def latest_purchases(self, limit: int = 10):
        cursor = self.connector.db["users"].find().sort("ultima_compra", -1).limit(limit)
        result = await cursor.to_list(length=None)
        print("Result in service latest_purchases:", result)
        return result

