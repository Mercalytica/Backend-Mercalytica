from services.modelService import ModelService
from validations.chatData import ChatData, ChatMessage
from services.chatBotService import ChatBotService
from fastapi.responses import JSONResponse
from typing import List
from rich import print


model_service = ChatBotService()


class ModelController:
    def __init__(self):
        self.collectionChat = ModelService()
        self.model_service = ChatBotService()

    async def create_new_chat(self, chat_data: ChatData):
        try:
            session_id = chat_data.id_session
            
            self.collectionChat.save_chat(chat_data)
            
            history_messages: List[ChatMessage] = self.collectionChat.get_messages_by_session_id(session_id)
            
            await self.model_service.load_model()
            
            # Llamamos al servicio del chatbot, pasándole el historial completo (memoria).
            response_content: str = await self.model_service.generate_response_with_history(history_messages)
            
            # Creamos el objeto para la respuesta de la IA.
            ai_message = ChatMessage(types="ai", message=response_content)
            
            # Guardamos la respuesta de la IA en la base de datos, usando una estructura de ChatData
            # que solo contenga el mensaje de la IA.
            ai_chat_data = ChatData(
                id_session=session_id,
                user_id=chat_data.user_id,
                messages=[ai_message]
            )
            self.collectionChat.save_chat(ai_chat_data)

            return JSONResponse(content={"response": response_content}, status_code=200)
            
        except Exception as e:
            print(f"[red]Error in create_new_chat: {e}[/red]")
            return JSONResponse(content={"error": "Failed to process chat"}, status_code=500)

    def get_chat_by_id(self, chat_id):
        return self.collectionChat.getChatById(chat_id)

    def get_all_chats(self):
        return self.collectionChat.getAllChats()
