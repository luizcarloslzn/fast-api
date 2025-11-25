from fastapi import FastAPI
from app.routers import produtos

app = FastAPI()

app.include_router(produtos.router)