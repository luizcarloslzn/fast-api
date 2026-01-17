from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.usuarios import Usuario
from app.database import get_db
import aiosqlite

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/")
async def listar(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: aiosqlite.Connection = Depends(get_db)
):
    offset = (page - 1) * limit

    cursor = await db.execute(
        "SELECT * FROM usuarios LIMIT ? OFFSET ?",
        (limit, offset)
    )
    usuarios = await cursor.fetchall()

    cursor_total = await db.execute("SELECT COUNT(*) FROM usuarios")
    total = (await cursor_total.fetchone())[0]

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit,
        "data": [dict(row) for row in usuarios]
    }


@router.post("/")
async def criar(usuario: Usuario, db: aiosqlite.Connection = Depends(get_db)):
    try:
        await db.execute(
            """
            INSERT INTO usuarios (
                id,
                name,
                email,
                password_hash,
                is_active,
                role
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                usuario.id,
                usuario.name,
                usuario.email,
                usuario.password_hash,
                usuario.is_active,
                usuario.role
            )
        )
        await db.commit()
        return usuario
    except Exception:
        raise HTTPException(400, "ID ou email já existe, ou erro ao salvar")


@router.get("/{usuario_id}")
async def buscar(usuario_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (usuario_id,)
    )
    usuario = await cursor.fetchone()

    if usuario is None:
        raise HTTPException(404, "Usuário não encontrado")

    return dict(usuario)


@router.put("/{usuario_id}")
async def atualizar(
    usuario_id: int,
    novo: Usuario,
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (usuario_id,)
    )
    existente = await cursor.fetchone()

    if existente is None:
        raise HTTPException(404, "Usuário não encontrado")

    await db.execute(
        """
        UPDATE usuarios
        SET
            id = ?,
            name = ?,
            email = ?,
            password_hash = ?,
            is_active = ?,
            role = ?
        WHERE id = ?
        """,
        (
            novo.id,
            novo.name,
            novo.email,
            novo.password_hash,
            novo.is_active,
            novo.role,
            usuario_id
        )
    )

    await db.commit()
    return novo


@router.delete("/{usuario_id}")
async def remover(usuario_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (usuario_id,)
    )
    existente = await cursor.fetchone()

    if existente is None:
        raise HTTPException(404, "Usuário não encontrado")

    await db.execute(
        "DELETE FROM usuarios WHERE id = ?",
        (usuario_id,)
    )
    await db.commit()

    return {"detail": "Usuário removido com sucesso"}