from services.modelService import ModelService
from validations.chatData import ChatData, ChatMessage
from services.chatBotService import ChatBotService
from fastapi import HTTPException
from typing import List, Tuple, Union


class ModelController:
    def __init__(self):
        # Asumiendo que ModelService maneja la base de datos (guardar historial)
        self.collectionChat = ModelService() 
        self.model_service = ChatBotService()

    async def create_new_chat(self, chat_data: ChatData) -> Tuple[str, Union[str, None]]:
        """
        Coordina la recepción del mensaje, la interacción con el LLM y el guardado.
        Devuelve la respuesta y el nombre del archivo PDF.
        """
        try:
            session_id = chat_data.id_session
            
            # 1. Guardar mensaje del usuario
            self.collectionChat.save_chat(chat_data)
            history_messages: List[ChatMessage] = self.collectionChat.get_messages_by_session_id(session_id)
            
            # 2. Cargar el modelo si es necesario
            if self.model_service.model is None:
                await self.model_service.load_model()
            
            # 3. Llamar al servicio y desempaquetar la tupla
            response_content, pdf_filename = await self.model_service.generate_response_with_history(history_messages)
            
            # 4. Guardar la respuesta de la IA
            ai_message = ChatMessage(types="ai", message=response_content)
            ai_chat_data = ChatData(
                id_session=session_id,
                user_id=chat_data.user_id,
                messages=[ai_message]
            )
            self.collectionChat.save_chat(ai_chat_data)

            # 5. DEVOLVER LA TUPLA para que el router la procese
            return response_content, pdf_filename
            
        except Exception as e:
            # Elevar HTTPException para que FastAPI lo maneje y devuelva un 500
            print(f"Error en create_new_chat: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Error interno en el procesamiento del chat: {str(e)}"
            )