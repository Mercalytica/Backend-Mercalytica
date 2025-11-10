# Proyecto Final: Solución de IA Basada en _Model Context Protocol (MCP)_

### Cátedra: **S.A.C. – Modelos y Aplicaciones de la Inteligencia Artificial**

---

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **Chatbot de Análisis Competitivo** que aplica principios de **Inteligencia Artificial (IA) Aplicada** para la gestión y contextualización avanzada de datos empresariales.

El sistema implementa el protocolo **Memory Contextual Protocol (MCP)**, el cual permite mantener una **coherencia conversacional profunda** entre interacciones, garantizando que las respuestas del modelo se mantengan contextualizadas a lo largo del diálogo.

---

## Aplicación

## **Nombre de la App:** (por definir)

## 🧩 Problemática

La problemática abordada consiste en que una empresa tecnológica dedicada a la comercialización de teléfonos celulares busca ampliar su alcance ingresando al ecosistema de Mercado Libre. Para optimizar su estrategia de expansión, la compañía requiere un análisis de mercado basado en inteligencia artificial que permita identificar cuáles son los modelos de teléfonos más vendidos y aquellos con mejores valoraciones por parte de los usuarios.
Este estudio tiene como objetivo proporcionar información estratégica que facilite decisiones de venta más precisas, orientadas a la demanda real y las preferencias del consumidor.

---

## Demo

_(Incluir GIF aquí una vez disponible)_

---

## Arquitectura General

La solución se estructura en tres capas principales:

1. **Interfaz Conversacional (Frontend)**
   Interacción directa con el usuario y visualización de resultados analíticos.

2. **Client (FastAPI + MCP)**
   Gestión de almacenamiento de los mensajes del chat por session

3. **Server**
   Gestion de recursos del modelo requiere para poder realizar las consultas

---

## ⚙️ Tecnologías y Librerías Utilizadas

| Librería / Framework              | Versión          | Descripción                                                                                                         |
| --------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| **FastAPI**                       | `0.121.1`        | Framework moderno y eficiente para construir APIs web en Python.                                                    |
| **Pydantic**                      | `2.12.4`         | Validación y configuración avanzada de datos, dependencia base de FastAPI.                                          |
| **LangChain / LangGraph**         | `1.0.x`          | Frameworks para desarrollar aplicaciones con _Large Language Models (LLMs)_ y flujos conversacionales inteligentes. |
| **Google AI Generative Language** | `0.9.0`          | Cliente oficial de Google para interactuar con modelos generativos como _Gemini_.                                   |
| **PyMongo / Motor**               | `4.15.3 / 3.7.1` | Conectores sincrónicos y asíncronos para _MongoDB_, utilizados para el manejo de datos.                             |
| **Requests**                      | `2.32.5`         | Librería estándar para realizar peticiones HTTP.                                                                    |
| **Uvicorn**                       | `0.38.0`         | Servidor ASGI utilizado para desplegar la aplicación FastAPI.                                                       |
| **fpdf**                          | `1.7.2`          | Generación de reportes y documentos en formato PDF.                                                                 |

---

## ⚙️ Instalación

```bash
 # 1️ Clonar el repositorio
git clone https://github.com/Mercalytica/Backend-Mercalytica
```

```bash
# 2 Moverse a la carpeta del proyecto

cd Backend-Mercalytica
```

```bash
# 3️ (Opcional) Crear y activar un entorno virtual

python -m venv venv
source venv/bin/activate # En macOS / Linux
venv\Scripts\activate # En Windows
```

```bash
# 4️ Instalar las dependencias

pip install -r requirements.txt
```

# Poner en marcha ambos servicios

```bash
 ##primero el de client

python ./client/main.py
```

```bash
 ## segundo  el de server

    python ./server/main.py
```

## Autores

- Atienza Jaqueline
- Cardenas Lucas
- DaSilva Felix
- Fleitas Selene

---
