from config.database import DatabaseConfig
from validations.chatData import ChatData,ChatMessage
from typing import List, Optional

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
   
     def getChatById(self, chat_id):
          chat = self.collectionChat.find_one({"_id": chat_id})
          return chat
     
     def getAllChats(self):
          chats = list(self.collectionChat.find())
          return chats