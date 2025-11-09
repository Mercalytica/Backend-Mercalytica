from fastapi import FastAPI
import uvicorn
from routers.modelRouter import modelRouter

app = FastAPI(title="Gestor de Competencia - Formosa", version="0.1.0")

app.include_router(modelRouter)

if __name__ == "__main__":
     uvicorn.run("main:app", host="0.0.0.0",port=5000,reload=True)