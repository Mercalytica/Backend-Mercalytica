from typing import Any, Dict, Union, List

def extraer_respuesta_aimessage(respuesta_modelo: Union[Dict[str, Any], Any]) -> str:
    """
    Interpreta un objeto de respuesta del modelo (AIMessage o diccionario) 
    y extrae el contenido de texto, manejando la nueva estructura de lista anidada.
    """
    
    contenido = None
    
    # 1. Manejo para el objeto AIMessage directo (e.g., de LangChain)
    if hasattr(respuesta_modelo, 'content'):
        contenido = respuesta_modelo.content
    
    # 2. Manejo para el formato de diccionario (como en tu código original)
    elif isinstance(respuesta_modelo, dict) and 'content' in respuesta_modelo:
        contenido = respuesta_modelo['content']
    
    # Si logramos extraer el contenido...
    if contenido is not None:
        
        # A. Si el 'content' es una lista (el nuevo caso que tienes)
        if isinstance(contenido, list) and contenido:
            # Buscamos el primer elemento y comprobamos si es un diccionario
            # con la clave 'text' (donde está tu respuesta real)
            primer_elemento = contenido[0]
            
            if isinstance(primer_elemento, dict) and 'text' in primer_elemento:
                return str(primer_elemento['text'])
            
            # Fallback por si la lista es simple (como en tu versión anterior)
            return str(primer_elemento)
        
        # B. Si el 'content' es una cadena de texto simple (caso estándar)
        return str(contenido)

    # 3. Manejo de fallback
    return f"Error: No se pudo extraer el contenido. Tipo de objeto recibido: {type(respuesta_modelo)}"