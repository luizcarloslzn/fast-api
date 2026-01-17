from pydantic import BaseModel
from datetime import datetime


class Usuario(BaseModel):
    id: int
    name: str
    email: str
    password_hash: str
    is_active: bool
    role: str
    created_at: datetime | None = None
    updated_at: datetime | None = None