from config.database import DatabaseConfig
from validations.chatData import ChatData,ChatMessage
from typing import List, Optional,Dict,Any
from fastapi import HTTPException
from bson import ObjectId

class ModelService:
     def __init__(self):
          db_config = DatabaseConfig()
          self.collectionChat = db_config.get_collection("chat_memory")
     
     def save_chat(self, chat_data: ChatData):
        if isinstance(chat_data.messages, ChatMessage):
            message_doc = chat_data.messages.dict()
        elif isinstance(chat_data.messages, list):
            message_doc = {"$each": [m.dict() for m in chat_data.messages]}
        else:
            raise ValueError("chat_data.messages debe ser ChatMessage o List[ChatMessage]")

        self.collectionChat.update_one(
            {"user_id": chat_data.user_id, "id_session": chat_data.id_session},
            {"$push": {"messages": message_doc}},
            upsert=True
        )
     
     def get_messages_by_session_id(self, id_session: str) -> List[ChatMessage]:
        chat_document = self.collectionChat.find_one(
            {"id_session": id_session},
            {"messages": 1, "_id": 0} 
        )
        
        if chat_document and 'messages' in chat_document:
            return [
                ChatMessage(types=msg['types'], message=msg['message'])
                for msg in chat_document['messages']
            ]
        
        return []
     
     @staticmethod
     def serialize_mongo_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte ObjectId a string en un documento de MongoDB para JSON."""
        if doc is None:
            return None
        
        serialized_doc = doc.copy() 
        
        # Convierte el ObjectId a string
        if "_id" in serialized_doc and isinstance(serialized_doc["_id"], ObjectId):
            serialized_doc["_id"] = str(serialized_doc["_id"])
            
        return serialized_doc
    
    # 🚨 MÉTODO getChatById CORREGIDO 🚨
     async def getChatById(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Busca y retorna TODAS las sesiones de chat asociadas a un user_id.
        Aplica serialización para convertir ObjectId a string.
        """
        try:
            # 1. Obtener el cursor
            chat_cursor = self.collectionChat.find({"user_id": user_id})
    
            # 2. Obtener la lista de documentos (Asumiendo PyMongo síncrono)
            chats = list(chat_cursor) 
    
            # 3. Serializar la lista usando el método estático
            # Llamamos al método estático usando el nombre de la clase (ModelService)
            serialized_chats = [ModelService.serialize_mongo_doc(chat) for chat in chats] 
    
            return serialized_chats
    
        except Exception as e:
            # En caso de un error de BD, elevamos la excepción.
            print(f"Error en ModelService.getChatById: {e}")
            # NOTA: Aquí solo se imprime el error, pero el Controller lo manejará
            # con HTTPException.
            return [] # Retorna lista vacía en caso de error de BD