from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.produtos import Produto
from app.database import get_db
import aiosqlite

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("/")
async def listar(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: aiosqlite.Connection = Depends(get_db)
):
    offset = (page - 1) * limit

    cursor = await db.execute(
        "SELECT * FROM produtos LIMIT ? OFFSET ?",
        (limit, offset)
    )
    produtos = await cursor.fetchall()

    cursor_total = await db.execute("SELECT COUNT(*) FROM produtos")
    total = (await cursor_total.fetchone())[0]

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit,
        "data": [dict(row) for row in produtos]
    }

@router.post("/")
async def criar(produto: Produto, db: aiosqlite.Connection = Depends(get_db)):
    try:
        await db.execute(
            "INSERT INTO produtos (id, nome, descricao, preco, quantidade) VALUES (?, ?, ?, ?, ?)",
            (produto.id, produto.nome, produto.descricao, produto.preco, produto.quantidade)
        )
        await db.commit()
        return produto
    except Exception:
        raise HTTPException(400, "ID já existe ou erro ao salvar")


@router.get("/{produto_id}")
async def buscar(produto_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (produto_id,)
    )
    produto = await cursor.fetchone()

    if produto is None:
        raise HTTPException(404, "Produto não encontrado")

    return dict(produto)


@router.put("/{produto_id}")
async def atualizar(produto_id: int, novo: Produto, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    existente = await cursor.fetchone()

    if existente is None:
        raise HTTPException(404, "Produto não encontrado")

    await db.execute("""
        UPDATE produtos 
        SET id = ?, nome = ?, descricao = ?, preco = ?, quantidade = ?
        WHERE id = ?
    """, (novo.id, novo.nome, novo.descricao, novo.preco, novo.quantidade, produto_id))

    await db.commit()
    return novo


@router.delete("/{produto_id}")
async def remover(produto_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    existente = await cursor.fetchone()

    if existente is None:
        raise HTTPException(404, "Produto não encontrado")

    await db.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    await db.commit()

    return {"detail": "Removido com sucesso"}