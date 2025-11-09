from datetime import datetime, timedelta

class OrdersServicer:
    def __init__(self, connector):
        self.connector = connector
        self.collection_name = "orders"

    # --- Consultas de Conteo y Total General ---

    async def total_orders(self):
        """Devuelve el número total de pedidos registrados en el sistema."""
        result = await self.connector.count(self.collection_name)
        return result

    async def total_revenue(self):
        """Calcula el ingreso total sumando el campo 'total' de todos los pedidos."""
        pipeline = [
            { "$group": {
                "_id": None,
                "total_revenue": { "$sum": "$total" }
            }},
            { "$project": { "_id": 0, "total_revenue": 1 } }
        ]
        result = await self.connector.aggregate(self.collection_name, pipeline)
        return result[0]['total_revenue'] if result else 0

    # --- Consultas de Estado y Agregación ---

    async def count_orders_by_status(self):
        """Agrupa y cuenta el número de pedidos por su estado (delivered, pending, etc.)."""
        pipeline = [{ "$group": { "_id": "$status", "count": { "$sum": 1 } } }]
        result = await self.connector.aggregate(self.collection_name, pipeline)
        return result

    async def average_order_total(self):
        """Calcula el valor promedio de los pedidos ('total')."""
        pipeline = [
            { "$group": {
                "_id": None,
                "average_total": { "$avg": "$total" }
            }},
            { "$project": { "_id": 0, "average_total": 1 } }
        ]
        result = await self.connector.aggregate(self.collection_name, pipeline)
        return result[0]['average_total'] if result else 0

    # --- Consultas de Filtro y Tiempo ---

    async def orders_by_status_and_time(self, status: str, days: int):
        """Cuenta pedidos con un estado específico ('status') realizados en los últimos N días."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = {
            "status": { "$regex": status, "$options": "i" },
            "ordered_at": { "$gte": cutoff_date }
        }
        
        result = await self.connector.db[self.collection_name].count_documents(query)
        return result

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
        
        result = await self.connector.aggregate(self.collection_name, pipeline)
        return result[0]['total_revenue_year'] if result else 0

    async def top_selling_products_by_quantity(self, limit: int = 10):
        """
        Identifica los productos más vendidos por cantidad ('quantity') total.
        Realiza una union (lookup/populate) con la colección de productos 
        para devolver información descriptiva (nombre, marca, categoría) 
        en lugar de solo el ID sensible.
        """
        pipeline = [
            # 1. Agrupar por product_id y sumar la cantidad total vendida.
            { "$group": { 
                "_id": "$product_id", 
                "total_quantity": { "$sum": "$quantity" } 
            }},
    
            # 2. Ordenar por la cantidad total (descendente).
            { "$sort": { "total_quantity": -1 } },
    
            # 3. Limitar a los N productos principales.
            { "$limit": limit },
    
            # 4. 'POPULATE' (Lookup): Unir con la colección de productos.
            #    Asume que el product_id en la orden coincide con el _id en la colección 'products'.
            #    La clave de unión es el _id (product_id agrupado).
            { "$lookup": {
                "from": "products", 
                "localField": "_id", 
                "foreignField": "_id", 
                "as": "product_details" 
            }},
    
            # 5. Desestructurar el array 'product_details'.
            { "$unwind": "$product_details" },
    
            # 6. Proyectar solo los datos no sensibles y relevantes.
            { "$project": { 
                "_id": 0, # Excluimos el _id sensible del producto de la salida (¡Seguridad!).
                "product_name": "$product_details.name",
                "product_brand": "$product_details.brand",
                "product_category": "$product_details.category",
                "total_quantity_sold": "$total_quantity" 
            }}
        ]
    
        try:
            # Asumiendo que self.collection es la colección de órdenes (Orders)
            result = await self.collection.aggregate(pipeline).to_list(length=limit)
            return result
        except Exception as e:
            # Manejo de errores
            print(f"Error executing pipeline for top selling products: {e}")
            return []