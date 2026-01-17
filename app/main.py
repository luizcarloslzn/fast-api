from fastapi import FastAPI
from app.routers import produtos, usuarios

app = FastAPI()

app.include_router(produtos.router)
app.include_router(usuarios.router)
