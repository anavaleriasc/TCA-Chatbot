from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user_repository import user


async def autenticar_usuario(
    session: AsyncSession,
    email: str,
    password: str,
):

    usuario = await user.get_by_email(
        session,
        email,
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos"
        )

    valid = user.verify_password(
        password,
        usuario.password_salt,
        usuario.hashed_password,
    )

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos"
        )

    return usuario