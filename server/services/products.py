class ProductsServicer:
    def __init__(self, connector):
        self.connector = connector
        self.collection_name = "products"

    async def total_products(self):
        """Devuelve el número total de productos publicados."""
        result = await self.connector.count(self.collection_name)
        print("Result in service total_products:", result)
        return result

    async def count_by_brand(self):
        """Agrupa y cuenta productos por marca (brand)."""
        pipeline = [{ "$group": { "_id": "$brand", "count": { "$sum": 1 } } }]
        result = await self.connector.aggregate(self.collection_name, pipeline)
        print("Result in service count_by_brand:", result)
        return result

    async def count_by_category(self):
        """Agrupa y cuenta productos por categoría (category)."""
        pipeline = [{ "$group": { "_id": "$category", "count": { "$sum": 1 } } }]
        result = await self.connector.aggregate(self.collection_name, pipeline)
        print("Result in service count_by_category:", result)
        return result

    async def count_by_shipping(self):
        """Agrupa y cuenta productos por tipo de envío (shipping)."""
        pipeline = [{ "$group": { "_id": "$shipping", "count": { "$sum": 1 } } }]
        result = await self.connector.aggregate(self.collection_name, pipeline)
        print("Result in service count_by_shipping:", result)
        return result
    
    async def products_in_stock(self, min_stock: int = 1):
        """Cuenta los productos que tienen un stock mayor o igual al valor mínimo."""
        query = { "stock": { "$gte": min_stock } }
        result = await self.connector.db[self.collection_name].count_documents(query)
        print("Result in service products_in_stock:", result)
        return result

    async def products_by_brand_and_category(self, brand: str, category: str):
        """Cuenta productos de una marca y categoría específicas (insensible a mayúsculas)."""
        query = {
            "brand": { "$regex": brand, "$options": "i" },
            "category": { "$regex": category, "$options": "i" }
        }
        result = await self.connector.db[self.collection_name].count_documents(query)
        print("Result in service products_by_brand_and_category:", result)
        return result

    async def products_by_price_range(self, min_price: float, max_price: float):
        """Cuenta productos dentro de un rango de precios (price)."""
        query = { "price": { "$gte": min_price, "$lte": max_price } }
        result = await self.connector.db[self.collection_name].count_documents(query)
        print("Result in service products_by_price_range:", result)
        return result

    async def free_shipping_by_reputation(self, reputation: str):
        """Cuenta los productos con envío 'Free' y una reputación de compañía específica."""
        query = {
            "shipping": { "$regex": "Free", "$options": "i" },
            "reputation": { "$regex": reputation, "$options": "i" }
        }
        result = await self.connector.db[self.collection_name].count_documents(query)
        print("Result in service free_shipping_by_reputation:", result)
        return result

    # --- Consultas de Listado y Ranking ---

    async def top_by_price(self, limit: int = 10):
        """Devuelve los productos más caros (orden descendente por price)."""
        cursor = self.connector.db[self.collection_name].find().sort("price", -1).limit(limit)
        result = await cursor.to_list(length=None)
        print("Result in service top_by_price:", result)
        return result
    
    async def top_by_price_ascending(self, limit: int = 10):
        """Devuelve los productos más baratos (orden ascendente por price)."""
        # Ordenamos por 'price' de forma ascendente (1) para obtener los más bajos.
        cursor = self.connector.db[self.collection_name].find().sort("price", 1).limit(limit)
        result = await cursor.to_list(length=None)
        return result

    async def latest_published(self, limit: int = 10):
        """Devuelve los productos publicados más recientemente."""
        cursor = self.connector.db[self.collection_name].find().sort("published_at", -1).limit(limit)
        result = await cursor.to_list(length=None)
        print("Result in service latest_published:", result)
        return result

    async def average_price_by_category(self):
        """Calcula el precio promedio de los productos agrupados por categoría."""
        pipeline = [
            { "$group": {
                "_id": "$category",
                "average_price": { "$avg": "$price" },
                "total_products": { "$sum": 1 }
            }}
        ]
        result = await self.connector.aggregate(self.collection_name, pipeline)
        print("Result in service average_price_by_category:", result)
        return result

    async def count_by_reputation(self):
        """Agrupa y cuenta productos por reputación de la compañía (reputation)."""
        pipeline = [{ "$group": { "_id": "$reputation", "count": { "$sum": 1 } } }]
        result = await self.connector.aggregate(self.collection_name, pipeline)
        print("Result in service count_by_reputation:", result)
        return result

    async def out_of_stock_products(self):
        """Cuenta los productos que actualmente tienen stock 0."""
        query = { "stock": 0 }
        result = await self.connector.db[self.collection_name].count_documents(query)
        print("Result in service out_of_stock_products:", result)
        return result

    async def recently_updated_products(self, days: int):
        """Devuelve los productos actualizados en los últimos N días."""
        # Calcula la fecha hace N días
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = { "updated_at": { "$gte": cutoff_date } }
        
        # Limitamos el resultado a 100 documentos por eficiencia, si se pide un número muy alto de días
        cursor = self.connector.db[self.collection_name].find(query).sort("updated_at", -1).limit(100)
        result = await cursor.to_list(length=None)
        
        print("Result in service recently_updated_products:", result)
        return result
    
    async def search_products(self, query: str, limit: int = 10):
        """
        Busca productos por nombre, marca o categoría utilizando una consulta de texto
        que ignora mayúsculas/minúsculas ($regex con $options: 'i').
    
        Devuelve los resultados clave del producto.
        """
        # 1. Configurar la consulta de expresión regular case-insensitive
        regex_query = {"$regex": query, "$options": "i"}
    
        # 2. Construir el filtro $or para buscar en name, brand o category
        filter_query = {
            "$or": [
                {"name": regex_query},
                {"brand": regex_query},
                {"category": regex_query}
            ]
        }
    
        # 3. Definir la proyección (qué campos devolver, excluyendo el _id sensible)
        projection = {
            "_id": 0, # Excluir ID sensible del producto
            "name": 1,
            "brand": 1,
            "category": 1,
            "price": 1,
            "stock": 1,
            "company_id": 1,
            "reputation": 1,
            "published_at": 1,
            "updated_at": 1,
        }
    
        try:
            # Asumiendo self.collection es la colección de productos
            cursor = self.collection.find(filter_query, projection).limit(limit)
            result = await cursor.to_list(length=limit)
            return result
        except Exception as e:
            print(f"Error en la búsqueda de productos: {e}")
            return []