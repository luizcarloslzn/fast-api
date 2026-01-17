from pydantic import BaseModel

class Produto(BaseModel):
    id: int
    nome: str
    descricao: str = None
    preco: float
    quantidade: int