from fastapi import APIRouter, HTTPException
from app.models import Produto
from app.database import ler_db, salvar_db

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/")
def listar():
    return ler_db()

@router.post("/")
def criar(produto: Produto):
    produtos = ler_db()
    if any(p["id"] == produto.id for p in produtos):
        raise HTTPException(400, "ID já existe")
    produtos.append(produto.dict())
    salvar_db(produtos)
    return produto

@router.get("/{produto_id}")
def buscar(produto_id: int):
    for p in ler_db():
        if p["id"] == produto_id:
            return p
    raise HTTPException(404, "Produto não encontrado")

@router.put("/{produto_id}")
def atualizar(produto_id: int, novo: Produto):
    produtos = ler_db()
    for i, p in enumerate(produtos):
        if p["id"] == produto_id:
            produtos[i] = novo.dict()
            salvar_db(produtos)
            return novo
    raise HTTPException(404, "Produto não encontrado")

@router.delete("/{produto_id}")
def remover(produto_id: int):
    produtos = ler_db()
    for i, p in enumerate(produtos):
        if p["id"] == produto_id:
            produtos.pop(i)
            salvar_db(produtos)
            return {"detail": "Removido com sucesso"}
    raise HTTPException(404, "Produto não encontrado")
