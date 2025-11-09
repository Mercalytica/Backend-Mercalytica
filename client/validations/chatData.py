from pydantic import BaseModel
from typing import List

class ChatMessage(BaseModel):
    types: str  
    message: str

class ChatData(BaseModel):
    id_session: str
    user_id: str
    messages: List[ChatMessage]

class ChatHistory(BaseModel):
    id_session: str
    user_id: str
    messages: List[ChatMessage]