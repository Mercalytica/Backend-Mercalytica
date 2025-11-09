from mcp.server import FastMCP
from services.users import UsersServicer
from db.connection import MongoConnector
from config.env import EnvConfig
from services.companies import CompaniesServicer
from services.products import ProductsServicer
from services.orders import OrdersServicer 
import logging

logging.getLogger("asyncio").setLevel(logging.WARNING)


# Inicialización del Framework y la Conexión a la Base de Datos
mcp = FastMCP("chatbot-server")

# Configuración de la conexión a Mongo (Asumiendo que EnvConfig maneja la URL)
urlMongo = EnvConfig().get("MONGO_URL")
connector = MongoConnector(urlMongo, "competition_manager")

# Inicialización de los Servidores de Datos
users_service = UsersServicer(connector)
companies_service = CompaniesServicer(connector)
products_service = ProductsServicer(connector)
orders_service = OrdersServicer(connector)

# ? ----------------- Herramientas relacionadas con usuarios 

@mcp.tool("contar_usuarios_por_tipo")
async def contar_usuarios_por_tipo():
    """Cuenta y agrupa usuarios por su tipo (comprador, vendedor, etc.)."""
    try:
        result = await users_service.count_by_type()
        return result if result else {"mensaje": "No se encontraron tipos de usuario."}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool("total_usuarios") 
async def total_usuarios():
    """Devuelve el número total de usuarios registrados en el sistema."""
    try:
        result = await users_service.total_users()
        return {"total": result}
    except Exception as error:
        print("Error en la herramienta: total_usuarios")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("usuarios_por_ubicacion") 
async def usuarios_por_ubicacion():
    """Agrupa y cuenta usuarios por su ubicación geográfica."""
    try:
        result = await users_service.users_by_location()
        return result if result else {"mensaje": "No se encontraron ubicaciones de usuario."}
    except Exception as error:
        print("Error en la herramienta: usuarios_por_ubicacion")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("usuarios_registrados_despues_de") 
async def usuarios_registrados_despues_de(year: int):
    """Cuenta el total de usuarios que se registraron después de un año dado."""
    try:
        result = await users_service.registered_after(year)
        return {"anio": year, "total": result}
    except Exception as error:
        print("Error en la herramienta: usuarios_registrados_despues_de")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("ultima_compra_en_anio")
async def ultima_compra_en_anio(year: int):
    """Cuenta los usuarios que realizaron su última compra dentro de un año específico."""
    try:
        result = await users_service.last_purchase_in_year(year)
        return {"anio": year, "total": result}
    except Exception as error:
        print("Error en la herramienta: ultima_compra_en_anio")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("compradores_por_ubicacion") 
async def compradores_por_ubicacion(location: str):
    """Cuenta los usuarios clasificados como 'compradores' en una ubicación dada."""
    try:
        result = await users_service.buyers_in_location(location)
        return {"ubicacion": location, "total": result}
    except Exception as error:
        print("Error en la herramienta: compradores_por_ubicacion")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("usuarios_registrados_en_empresa_anio")
async def usuarios_registrados_en_empresa_anio(empresa: str, year: int):
    """Cuenta los usuarios registrados en una empresa específica y después de un año dado."""
    try:
        result = await users_service.registered_in_company_year(empresa, year)
        # Se renombra 'año' por 'anio' en el diccionario de retorno para consistencia.
        return {"empresa": empresa, "anio": year, "total": result}
    except Exception as error:
        print("Error en la herramienta: usuarios_registrados_en_empresa_anio")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}


# ? ----------------- Herramientas relacionadas con las compañías 

@mcp.tool("total_companias")
async def total_companias():
    """Devuelve el número total de compañías registradas."""
    try:
        result = await companies_service.total_companies()
        return {"total": result}
    except Exception as error:
        print("Error en la herramienta: total_companias")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("contar_companias_por_tipo")
async def contar_companias_por_tipo():
    """Agrupa y cuenta compañías por su tipo."""
    try:
        result = await companies_service.count_by_type()
        return result if result else {"mensaje": "No se encontraron tipos de compañía."}
    except Exception as error:
        print("Error en la herramienta: contar_companias_por_tipo")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("companias_por_ubicacion")
async def companias_por_ubicacion():
    """Agrupa y cuenta compañías por su ubicación."""
    try:
        result = await companies_service.companies_by_location()
        return result if result else {"mensaje": "No se encontraron ubicaciones de compañía."}
    except Exception as error:
        print("Error en la herramienta: companias_por_ubicacion")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("companias_por_reputacion") 
async def companias_por_reputacion():
    """Agrupa y cuenta compañías por su reputación."""
    try:
        result = await companies_service.companies_by_reputation()
        return result if result else {"mensaje": "No se encontraron reputaciones de compañía."}
    except Exception as error:
        print("Error en la herramienta: companias_por_reputacion")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("companias_registradas_despues_de")
async def companias_registradas_despues_de(year: int):
    """Cuenta compañías registradas después de un año dado."""
    try:
        result = await companies_service.registered_after(year)
        return {"anio": year, "total": result}
    except Exception as error:
        print("Error en la herramienta: companias_registradas_despues_de")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("companias_activas_en_anio")
async def companias_activas_en_anio(year: int):
    """Cuenta compañías con actividad (actualizadas) en un año dado."""
    try:
        result = await companies_service.active_in_year(year)
        return {"anio": year, "total": result}
    except Exception as error:
        print("Error en la herramienta: companias_activas_en_anio")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("contar_companias_por_tipo_y_ubicacion")
async def contar_companias_por_tipo_y_ubicacion(company_type: str, location: str):
    """Cuenta compañías de un tipo y ubicación específicos."""
    try:
        result = await companies_service.count_by_type_and_location(company_type, location)
        return {"tipo": company_type, "ubicacion": location, "total": result}
    except Exception as error:
        print("Error en la herramienta: contar_companias_por_tipo_y_ubicacion")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("companias_alto_volumen_ventas")  
async def companias_alto_volumen_ventas(min_volume: int):
    """Cuenta las compañías con un volumen de ventas superior o igual al mínimo dado."""
    try:
        result = await companies_service.high_sales_volume(min_volume)
        return {"volumen_minimo": min_volume, "total": result}
    except Exception as error:
        print("Error en la herramienta: companias_alto_volumen_ventas")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("top_companias_por_ventas") 
async def top_companias_por_ventas(limit: int = 10):
    """Devuelve las N compañías con mayor volumen de ventas."""
    try:
        result = await companies_service.top_by_sales_volume(limit)
        return result
    except Exception as error:
        print("Error en la herramienta: top_companias_por_ventas")
        print(error)
        return {"msg": "Error inesperado, por favor intente de nuevo"}

# ? ----------------- herramientas relacionadas con los productos del mercado  

@mcp.tool("total_productos") 
async def total_productos():
    """Devuelve el número total de productos disponibles."""
    try:
        result = await products_service.total_products()
        return {"total": result}
    except Exception as error:
        print(f"Error en la herramienta: total_productos: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("contar_productos_por_marca") 
async def contar_productos_por_marca():
    """Agrupa y cuenta productos por marca."""
    try:
        result = await products_service.count_by_brand()
        return result if result else {"mensaje": "No se encontraron marcas."}
    except Exception as error:
        print(f"Error en la herramienta: contar_productos_por_marca: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("contar_productos_por_categoria") 
async def contar_productos_por_categoria():
    """Agrupa y cuenta productos por categoría."""
    try:
        result = await products_service.count_by_category()
        return result if result else {"mensaje": "No se encontraron categorías."}
    except Exception as error:
        print(f"Error en la herramienta: contar_productos_por_categoria: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("productos_en_stock") 
async def productos_en_stock(min_stock: int = 1):
    """Cuenta los productos con stock mayor o igual al mínimo dado."""
    try:
        result = await products_service.products_in_stock(min_stock)
        return {"stock_minimo": min_stock, "total": result}
    except Exception as error:
        print(f"Error en la herramienta: productos_en_stock: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("productos_por_marca_y_categoria") 
async def productos_por_marca_y_categoria(brand: str, category: str):
    """Cuenta productos de una marca y categoría específicas."""
    try:
        result = await products_service.products_by_brand_and_category(brand, category)
        return {"marca": brand, "categoria": category, "total": result}
    except Exception as error:
        print(f"Error en la herramienta: productos_por_marca_y_categoria: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("productos_por_rango_precio") 
async def productos_por_rango_precio(min_price: float, max_price: float):
    """Cuenta productos dentro de un rango de precios dado."""
    try:
        result = await products_service.products_by_price_range(min_price, max_price)
        return {"precio_min": min_price, "precio_max": max_price, "total": result}
    except Exception as error:
        print(f"Error en la herramienta: productos_por_rango_precio: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("top_productos_mas_caros") 
async def top_productos_mas_caros(limit: int = 10):
    """Devuelve los N productos con el precio más alto (más caros)."""
    try:
        result = await products_service.top_by_price(limit)
        return result
    except Exception as error:
        print(f"Error en la herramienta: top_productos_mas_caros: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("productos_publicados_recientemente") 
async def productos_publicados_recientemente(limit: int = 10):
    """Devuelve los N productos publicados más recientemente."""
    try:
        result = await products_service.latest_published(limit)
        return result
    except Exception as error:
        print(f"Error en la herramienta: productos_publicados_recientemente: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("precio_promedio_por_categoria") 
async def precio_promedio_por_categoria():
    """Calcula el precio promedio de los productos agrupados por categoría."""
    try:
        result = await products_service.average_price_by_category()
        return result if result else {"mensaje": "No hay datos para calcular el promedio."}
    except Exception as error:
        print(f"Error en la herramienta: precio_promedio_por_categoria: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("contar_productos_por_reputacion") 
async def contar_productos_por_reputacion():
    """Agrupa y cuenta productos por reputación de la compañía."""
    try:
        result = await products_service.count_by_reputation()
        return result if result else {"mensaje": "No se encontraron reputaciones."}
    except Exception as error:
        print(f"Error en la herramienta: contar_productos_por_reputacion: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("productos_sin_stock") 
async def productos_sin_stock():
    """Cuenta el número total de productos con stock cero."""
    try:
        result = await products_service.out_of_stock_products()
        return {"total": result}
    except Exception as error:
        print(f"Error en la herramienta: productos_sin_stock: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("productos_actualizados_recientemente") 
async def productos_actualizados_recientemente(days: int):
    """Devuelve los productos actualizados en los últimos N días (máx. 100)."""
    try:
        result = await products_service.recently_updated_products(days)
        return result
    except Exception as error:
        print(f"Error en la herramienta: productos_actualizados_recientemente: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("top_productos_mas_baratos") 
async def top_productos_mas_baratos(limit: int = 10):
    """Devuelve los N productos con el precio más bajo (más baratos)."""
    try:
        result = await products_service.top_by_price_ascending(limit)
        return result
    except Exception as error:
        print(f"Error en la herramienta: top_productos_mas_baratos: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("buscar_productos") 
async def buscar_productos(query: str, limit: int = 10):
    """Busca productos por nombre, marca o categoría usando un término de búsqueda case-insensitive."""
    try:
        result = await products_service.search_products(query, limit)
        return result
    except Exception as error:
        print(f"Error en la herramienta: buscar_productos: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

# ? ----------------- herramientas relacionadas con los pedidos (ÓRDENES) 

@mcp.tool("total_pedidos")
async def total_pedidos():
    """Devuelve el número total de pedidos (órdenes) realizados en el sistema."""
    try:
        result = await orders_service.total_orders()
        return {"total_pedidos": result}
    except Exception as error:
        print(f"Error en la herramienta: total_pedidos: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("ingreso_total")
async def ingreso_total():
    """Calcula el ingreso total (revenue) sumado de todos los pedidos."""
    try:
        result = await orders_service.total_revenue()
        return {"ingreso_total": result}
    except Exception as error:
        print(f"Error en la herramienta: ingreso_total: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("contar_pedidos_por_estado")
async def contar_pedidos_por_estado():
    """Agrupa y cuenta la cantidad de pedidos por su estado (ej: 'delivered', 'pending')."""
    try:
        result = await orders_service.count_orders_by_status()
        return result if result else {"mensaje": "No se encontraron estados de pedido."}
    except Exception as error:
        print(f"Error en la herramienta: contar_pedidos_por_estado: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("promedio_total_pedido")
async def promedio_total_pedido():
    """Calcula el valor promedio de las órdenes (total de la orden)."""
    try:
        result = await orders_service.average_order_total()
        return {"promedio_total_pedido": result}
    except Exception as error:
        print(f"Error en la herramienta: promedio_total_pedido: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("pedidos_por_estado_y_tiempo")
async def pedidos_por_estado_y_tiempo(status: str, days: int):
    """Cuenta pedidos con un estado específico realizados en los últimos N días."""
    try:
        result = await orders_service.orders_by_status_and_time(status, days)
        return {"estado": status, "dias": days, "total": result}
    except Exception as error:
        print(f"Error en la herramienta: pedidos_por_estado_y_tiempo: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("ingreso_total_por_anio") 
async def ingreso_total_por_anio(year: int):
    """Calcula el ingreso total generado por pedidos en un año específico."""
    try:
        result = await orders_service.revenue_by_year(year)
        return {"anio": year, "ingreso_total": result}
    except Exception as error:
        print(f"Error en la herramienta: ingreso_total_por_anio: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

@mcp.tool("top_productos_mas_vendidos")
async def top_productos_mas_vendidos(limit: int = 10):
    """Identifica y devuelve los IDs de los N productos más vendidos por cantidad total."""
    try:
        result = await orders_service.top_selling_products_by_quantity(limit)
        return result
    except Exception as error:
        print(f"Error en la herramienta: top_productos_mas_vendidos: {error}")
        return {"msg": "Error inesperado, por favor intente de nuevo"}

if __name__ == "__main__":
    mcp.run(transport="streamable-http")