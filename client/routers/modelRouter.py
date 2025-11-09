from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse 

from controllers.modelController import ModelController
from validations.chatData import ChatData
from services.chatBotService import PDF_DIR # Importar la ubicación del directorio PDF
import os 


modelRouter = APIRouter(prefix="/api") # Añadido /api al prefijo para organizar
controller = ModelController() 

# 1. ENDPOINT PRINCIPAL DE CHAT
@modelRouter.post("/chatBot", tags=["ChatBots"])
async def create_chat(chat_data: ChatData):
    """
    Envía un mensaje al modelo, recibe la respuesta y devuelve
    la URL de descarga si se generó un reporte PDF.
    """
    # El controlador devuelve la tupla (response_text, pdf_filename)
    response_text, pdf_filename = await controller.create_new_chat(chat_data)
    
    response_data = {
        "message": response_text,
        "pdf_url": None  # Por defecto no hay PDF
    }
    
    # Si se generó un PDF, adjuntamos la URL de descarga
    if pdf_filename:
        # Construye la URL completa que apunta al endpoint de descarga
        response_data["pdf_url"] = f"/api/reports/download/{pdf_filename}"
        
    return response_data

# 2. ENDPOINT DE DESCARGA DE PDF
@modelRouter.get("/reports/download/{filename:path}", tags=["Reports"])
async def download_report(filename: str):
    """
    Permite la descarga de un reporte PDF generado previamente.
    """
    file_path = os.path.join(PDF_DIR, filename)
    
    # Verificación de seguridad: El archivo debe existir
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404, 
            detail="El reporte solicitado no se encuentra."
        )
    
    # Devolver el archivo usando FileResponse
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/pdf'
    )

@modelRouter.get("/chatBot/history/{session_id}", tags=["ChatBots"])
async def get_chat_history(session_id: str):
    """
    Recupera el historial de mensajes de una sesión existente usando 
    el ID de sesión como parámetro de ruta.
    """
    # Llamamos al controlador pasándole directamente el session_id
    history = await controller.getSeccionBySession(session_id)
    
    # Devuelve la lista de objetos ChatMessage
    return history

@modelRouter.get("/chatBot/myHistory/{user_id}", tags=["ChatBots"])
async def get_chat_history(user_id: str):
    history = await controller.getChatsById(user_id)
    return history