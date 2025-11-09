from config.llm import getModel
from helpers.extractResponse import extraer_respuesta_aimessage
from validations.chatData import ChatMessage # Asegúrate de importar ChatMessage
from typing import List
from rich import print


class ChatBotService:
    def __init__(self):
        self.model = None

    async def load_model(self):
        self.model = await getModel()
        if self.model is None:
            raise RuntimeError("El modelo no se pudo cargar. getModel() devolvió None.")

    async def generate_response_with_history(self, history_messages: List[ChatMessage]):
        if self.model is None:
            return RuntimeError("No se puede generar respuesta: el modelo no está cargado.")
        
        # 1. Definir el System Prompt
        SYSTEM_PROMPT = """
        Eres un Asistente Analítico de Mercado (AAM).
        Tu personalidad es formal, profesional y excepcionalmente servicial.
        
        Regla Principal: Tu objetivo primordial es analizar las consultas de mercado del usuario
        y determinar la herramienta analítica más adecuada para ejecutarlas.
        
        Restricciones de Conversación:
        1.  Si la consulta es un saludo, una despedida, o una pregunta simple sobre tu identidad (ej: '¿Quién eres?'), responde de manera breve, cortés y humana, manteniendo siempre tu tono profesional.
        2.  Si la consulta NO es social y NO puede ser respondida con una de tus herramientas (ej: '¿Qué opina del clima?'), indica de manera concisa que esa información está fuera de tu alcance analítico.
        3.  Asegúrate de que las respuestas de las herramientas sean precisas, profesionales y se presenten con claridad.
        4.  GESTIÓN DE CONTEXTO Y MEMORIA: Si el usuario hace referencia a información de una conversación pasada que ya no se encuentra en el contexto actual, indícale de forma cortés que esa información previa no está disponible. Explica que es posible que se haya iniciado una nueva sesión o que el historial haya superado el límite de memoria. En ese caso, sugiere al usuario revisar el menú de historial (el que se encuentra a la derecha de la plataforma) para localizar la sesión anterior.
        5.  Si el usuairo pregunta sobre tu accion con una herrameitan simpre verifica antes de respoder puede ser que ya se halla actualizado tu servicio de obtener informacion
        """
        
        # 2. Construir la lista de mensajes con el System Prompt al inicio
        formatted_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        
        # 3. Formatear los mensajes del historial (Memoria)
        for msg in history_messages:
            # Mapeamos 'types' ('user', 'ai') a 'role' ('user', 'assistant')
            role = "user" if msg.types == "user" else "assistant"
            
            formatted_messages.append({
                "role": role,
                "content": msg.message
            })
            
        # 4. Invocar al modelo con la secuencia completa (System Prompt + Historial)
        response = await self.model.ainvoke({
             "messages": formatted_messages
         })
        
        print(response)
        
        print(response)
        print(extraer_respuesta_aimessage(response["messages"][-1]))
        
        return extraer_respuesta_aimessage(response["messages"][-1])
