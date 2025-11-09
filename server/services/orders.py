from datetime import datetime, timedelta

class OrdersServicer:
    def __init__(self, connector):
        self.connector = connector
        self.collection_name = "orders"

    # --- Consultas de Conteo y Total General ---

    async def total_orders(self):
        """Devuelve el número total de pedidos registrados en el sistema."""
        try:
            result = await self.connector.count(self.collection_name)
            return result
        except Exception as e:
            print(f"Error en total_orders: {e}")
            return 0

    async def total_revenue(self):
        """Calcula el ingreso total sumando el campo 'total' de todos los pedidos."""
        pipeline = [
            { "$group": {
                "_id": None,
                "total_revenue": { "$sum": "$total" }
            }},
            { "$project": { "_id": 0, "total_revenue": 1 } }
        ]
        try:
            result = await self.connector.aggregate(self.collection_name, pipeline)
            return result[0]['total_revenue'] if result else 0
        except Exception as e:
            print(f"Error en total_revenue: {e}")
            return 0

    # --- Consultas de Estado y Agregación ---

    async def count_orders_by_status(self):
        """Agrupa y cuenta el número de pedidos por su estado (delivered, pending, etc.)."""
        pipeline = [{ "$group": { "_id": "$status", "count": { "$sum": 1 } } }]
        try:
            result = await self.connector.aggregate(self.collection_name, pipeline)
            return result
        except Exception as e:
            print(f"Error en count_orders_by_status: {e}")
            return []

    async def average_order_total(self):
        """Calcula el valor promedio de los pedidos ('total')."""
        pipeline = [
            { "$group": {
                "_id": None,
                "average_total": { "$avg": "$total" }
            }},
            { "$project": { "_id": 0, "average_total": 1 } }
        ]
        try:
            result = await self.connector.aggregate(self.collection_name, pipeline)
            return result[0]['average_total'] if result else 0
        except Exception as e:
            print(f"Error en average_order_total: {e}")
            return 0

    # --- Consultas de Filtro y Tiempo ---

    async def orders_by_status_and_time(self, status: str, days: int):
        """Cuenta pedidos con un estado específico ('status') realizados en los últimos N días."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Asumiendo que self.connector.db es accesible
        collection = self.connector.db[self.collection_name] 
        
        query = {
            "status": { "$regex": status, "$options": "i" },
            "ordered_at": { "$gte": cutoff_date }
        }
        
        try:
            result = await collection.count_documents(query)
            return result
        except Exception as e:
            print(f"Error en orders_by_status_and_time: {e}")
            return 0

    async def revenue_by_year(self, year: int):
        """Calcula el ingreso total ('total') para pedidos realizados en un año específico."""
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)
        
        pipeline = [
            { "$match": { 
                "ordered_at": { "$gte": start_date, "$lt": end_date } 
            }},
            { "$group": { 
                "_id": None, 
                "total_revenue_year": { "$sum": "$total" } 
            }},
            { "$project": { "_id": 0, "total_revenue_year": 1 } }
        ]
        
        try:
            result = await self.connector.aggregate(self.collection_name, pipeline)
            return result[0]['total_revenue_year'] if result else 0
        except Exception as e:
            print(f"Error en revenue_by_year: {e}")
            return 0

    # --- Consulta Compleja (Corregida) ---

    async def top_selling_products_by_quantity(self, limit: int = 10):
        """Identifica los productos más vendidos y enriquece la información con la colección 'products'."""
        
        pipeline = [
            # 1. Agrupar por product_id y sumar la cantidad total vendida.
            { "$group": { 
                "_id": "$product_id", 
                "total_quantity": { "$sum": "$quantity" } 
            }},
            
            # 2. 🚨 CORRECCIÓN TIPO: Asegura que el _id agrupado sea un ObjectID para el lookup.
            { "$addFields": { 
                "_id": { "$toObjectId": "$_id" } 
            }},
            
            # 3. Ordenar por la cantidad total (descendente).
            { "$sort": { "total_quantity": -1 } },
            
            # 4. Limitar a los N productos principales.
            { "$limit": limit },
            
            # 5. Lookup: Unión con 'products'.
            { "$lookup": {
                "from": "products", 
                "localField": "_id", 
                "foreignField": "_id", 
                "as": "product_details" 
            }},
            
            # 6. Desestructurar el array 'product_details'.
            { "$unwind": "$product_details" },
            
            # 7. Proyectar solo los datos relevantes.
            { "$project": { 
                "_id": 0, 
                "product_name": "$product_details.name",
                "product_brand": "$product_details.brand",
                "product_category": "$product_details.category",
                "total_quantity_sold": "$total_quantity" 
            }}
        ]
        
        try:
            # Asumiendo que self.collection es la colección de órdenes (Orders)
            result = await self.connector.aggregate(self.collection_name, pipeline)
            # Imprimir para depuración (Debugging)
            print(f"Resultado de top_selling_products_by_quantity: {result}") 
            return result
        except Exception as e:
            # Si el error está aquí, el mensaje nos indicará qué falló en la agregación.
            print(f"Error ejecutando top_selling_products_by_quantity: {e}")
            return []