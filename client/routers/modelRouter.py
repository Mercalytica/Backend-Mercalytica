from fastapi import APIRouter
from controllers.modelController import ModelController
from validations.chatData import ChatData

modelRouter = APIRouter()
controller = ModelController()

@modelRouter.post("/chatBot", tags=["ChatBots"])
async def create_chat(chat_data: ChatData):
    return await controller.create_new_chat(chat_data)