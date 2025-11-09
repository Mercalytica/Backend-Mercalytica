from config.llm import getModel
from helpers.extractResponse import extraer_respuesta_aimessage
from validations.chatData import ChatMessage 
from typing import List, Tuple, Union
import datetime
import os 
from fpdf import FPDF # Librería para PDF
from rich import print

# Directorio donde guardaremos los PDFs generados
PDF_DIR = "reports_generated"
os.makedirs(PDF_DIR, exist_ok=True) # Crea el directorio si no existe

class ChatBotService:
    def __init__(self):
        self.model = None
        self.fecha_actual = datetime.datetime.now()

    async def load_model(self):
        self.model = await getModel()
        if self.model is None:
            # Eleva una excepción si no se puede cargar el modelo
            raise RuntimeError("El modelo no se pudo cargar. getModel() devolvió None.")

    async def generate_response_with_history(self, history_messages: List[ChatMessage]) -> Tuple[str, Union[str, None]]:
        """
        Genera la respuesta del modelo y el PDF si se solicita un reporte.
        Devuelve (response_text, pdf_filename)
        """
        if self.model is None:
            raise RuntimeError("No se puede generar respuesta: el modelo no está cargado. Llama a load_model() primero.")
        
        try:
            # 1. Definir el System Prompt para guiar al modelo
            SYSTEM_PROMPT = f"""
            Eres un Asistente Analítico de Mercado (AAM). Tu rol es proporcionar análisis concisos, precisos y profesionales.

		  **REGLAS Y FUNCIONALIDAD:**
		  
		  1. Rol: Actúa siempre como un analista profesional.
		  2. Memoria: Mantén la coherencia con el historial de la sesión.
		  
		  **GENERACIÓN DE REPORTE (PDF):**
		  
		  3. Si el usuario solicita un reporte formal o análisis completo, debes iniciar la respuesta **EXACTAMENTE** con la etiqueta: **[REPORTE_INICIADO]**.
		  4. NO uses la etiqueta `[REPORTE_INICIADO]` para consultas informales.
		  5. La fecha para cualquier reporte es: [Insertar fecha actual aquí].
		  
		  **FORMATO DEL TEXTO (CRÍTICO - PARA PDF BÁSICO):**
		  
		  6. **INICIO:** Después de la etiqueta `[REPORTE_INICIADO]`, **NO añadas símbolos decorativos (ej: ***,****, ---) ni líneas vacías.** Comienza el texto del reporte inmediatamente en la siguiente línea.
		  7. **NO uses formato Markdown.** Esto incluye: NO usar negritas (`**`), cursivas (`*`), ni listas con guiones o asteriscos (`-`, `*`).
		  8. **Estructura Visual:** Para simular encabezados y secciones, usa **TEXTO EN MAYÚSCULAS** y separa los párrafos y secciones con un doble salto de línea (dos `ENTER`).
		  
		  **OBJETIVO:** El texto entregado debe ser un bloque limpio, plano y estructurado únicamente con mayúsculas y saltos de línea.
            """
            
            # 2. Construir la lista de mensajes (System Prompt + Historial)
            formatted_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for msg in history_messages:
                role = "user" if msg.types == "user" else "assistant"
                formatted_messages.append({"role": role, "content": msg.message})
                
            # 3. Invocar al modelo
            response = await self.model.ainvoke({"messages": formatted_messages})
		  
            print(response)
            
		  # 4. Extraer la respuesta (Asegúrate de que esta función maneje errores y siempre devuelva un string)
            response_text = extraer_respuesta_aimessage(response["messages"][-1])
            
            print(response_text)

            
            
            pdf_filename = None
            
            # 5. Lógica de Detección de Reporte y Generación de PDF
            if "[REPORTE_INICIADO]" in response_text:
                pdf_content = response_text.replace("[REPORTE_INICIADO]", "").strip()
                
                # Generar el PDF
                pdf_filename = self._generate_report_pdf(pdf_content)
                
                # Modificar la respuesta al usuario para indicar que el PDF fue creado
                response_text = f"**[PDF Creado]**\nSu análisis ha sido completado y generado en formato PDF. Puede descargarlo a través del enlace.\n\n{pdf_content}"
            
            return response_text, pdf_filename

        except Exception as e:
            # En caso de error, devuelve un mensaje de error y no se genera PDF
            print(f"Error en generate_response_with_history: {e}")
            return f"ERROR: Fallo al procesar la solicitud del modelo. Por favor, inténtelo de nuevo. Detalle: {str(e)}", None
  
    def _generate_report_pdf(self, content: str) -> str:
        """Función interna para crear y guardar el archivo PDF."""
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_title('Reporte de Análisis de Mercado (AAM)')
        
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 15, 'Reporte Analítico Generado por AAM', 0, 1, 'C')

        fecha_hora = self.fecha_actual.strftime("%d-%m-%Y %H:%M:%S")
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 5, f'Fecha de Generación: {fecha_hora}', 0, 1, 'R')
        pdf.ln(5)

        pdf.set_font('Arial', '', 12)
        # Usar utf-8 para manejar caracteres especiales
        pdf.multi_cell(0, 7, content) 

        timestamp = self.fecha_actual.strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_analisis_{timestamp}.pdf"
        full_path = os.path.join(PDF_DIR, filename)
        pdf.output(full_path)
        
        return filename