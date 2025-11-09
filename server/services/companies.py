from datetime import datetime

class CompaniesServicer:
    def __init__(self, connector):
        self.connector = connector
        self.collection_name = "companies"

    async def total_companies(self):
        """Devuelve el número total de compañías registradas."""
        result = await self.connector.count(self.collection_name)
        print("Result in service total_companies:", result)
        return result

    async def count_by_type(self):
        """Agrupa y cuenta compañías por su tipo (type)."""
        pipeline = [{ "$group": { "_id": "$type", "count": { "$sum": 1 } } }]
        result = await self.connector.aggregate(self.collection_name, pipeline)
        print("Result in service count_by_type:", result)
        return result

    async def companies_by_location(self):
        """Agrupa y cuenta compañías por su ubicación (location)."""
        pipeline = [{ "$group": { "_id": "$location", "count": { "$sum": 1 } } }]
        result = await self.connector.aggregate(self.collection_name, pipeline)
        print("Result in service companies_by_location:", result)
        return result

    async def companies_by_reputation(self):
        """Agrupa y cuenta compañías por su reputación (reputation)."""
        pipeline = [{ "$group": { "_id": "$reputation", "count": { "$sum": 1 } } }]
        result = await self.connector.aggregate(self.collection_name, pipeline)
        print("Result in service companies_by_reputation:", result)
        return result
    
    
    async def registered_after(self, year: int):
        """Cuenta las compañías registradas después del 1 de enero del año dado."""
        start_date = datetime(year, 1, 1)
        query = { "registered_at": { "$gt": start_date } }
        result = await self.connector.db[self.collection_name].count_documents(query)
        print("Result in service registered_after:", result)
        return result

    async def active_in_year(self, year: int):
        """Cuenta las compañías con actividad (last_activity) en el año dado."""
        start_year = datetime(year, 1, 1)
        end_year = datetime(year + 1, 1, 1)
        query = { "last_activity": { "$gte": start_year, "$lt": end_year } }
        result = await self.connector.db[self.collection_name].count_documents(query)
        print("Result in service active_in_year:", result)
        return result

    async def count_by_type_and_location(self, company_type: str, location: str):
        """Cuenta compañías de un tipo y ubicación específicos (insensible a mayúsculas)."""
        query = {
            "type": { "$regex": company_type, "$options": "i" },
            "location": { "$regex": location, "$options": "i" }
        }
        result = await self.connector.db[self.collection_name].count_documents(query)
        print("Result in service count_by_type_and_location:", result)
        return result

    async def high_sales_volume(self, min_volume: int):
        """Cuenta las compañías con un volumen de ventas (sales_volume) superior o igual al mínimo dado."""
        query = { "sales_volume": { "$gte": min_volume } }
        result = await self.connector.db[self.collection_name].count_documents(query)
        print("Result in service high_sales_volume:", result)
        return result

    async def reputation_in_location(self, reputation: str, location: str):
        """Cuenta compañías con una reputación y ubicación dadas (insensible a mayúsculas)."""
        query = {
            "reputation": { "$regex": reputation, "$options": "i" },
            "location": { "$regex": location, "$options": "i" }
        }
        result = await self.connector.db[self.collection_name].count_documents(query)
        print("Result in service reputation_in_location:", result)
        return result


    async def top_by_sales_volume(self, limit: int = 10):
        """Devuelve las compañías con mayor volumen de ventas."""
        cursor = self.connector.db[self.collection_name].find().sort("sales_volume", -1).limit(limit)
        result = await cursor.to_list(length=None)
        print("Result in service top_by_sales_volume:", result)
        return result

    async def latest_active(self, limit: int = 10):
        """Devuelve las compañías con la actividad más reciente."""
        cursor = self.connector.db[self.collection_name].find().sort("last_activity", -1).limit(limit)
        result = await cursor.to_list(length=None)
        print("Result in service latest_active:", result)
        return result