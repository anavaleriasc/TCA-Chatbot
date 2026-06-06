from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db

from schemas.auth_schema import (
    LoginRequest,
)

from services.auth_service import (
    autenticar_usuario,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):

    usuario = await autenticar_usuario(
        db,
        payload.email,
        payload.password,
    )

    return {
        "message": "Login realizado com sucesso",
        "user_id": usuario.id,
        "email": usuario.email,
    }