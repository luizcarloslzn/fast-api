from pydantic import BaseModel

class Produto(BaseModel):
    id: int
    descricao: str = None
    nome: str
    preco: float
    quantidade: int
