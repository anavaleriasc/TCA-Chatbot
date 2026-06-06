from models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Iterable, Optional
from sqlalchemy import select
import hashlib
import hmac
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional




class UserRepository:
    def create_password_hash(
        self,
        password: str,
    ) -> tuple[str, str]:

        salt = os.urandom(16).hex()

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            100_000,
        ).hex()

        return salt, password_hash

    def verify_password(
        self,
        password: str,
        salt: str,
        stored_hash: str,
    ) -> bool:

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            100_000,
        ).hex()

        return hmac.compare_digest(
            password_hash,
            stored_hash,
        )

    async def create(self,session:AsyncSession, *, email:str, password:str )->User:
        salt, hash_password = self.create_password_hash(
            password
        )

        user = User(
            email=email,
            hashed_password=hash_password,
            password_salt=salt,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def update(self,session:AsyncSession,
     user:User, 
     *, 
     email:Optional[str]=None, 
     password: Optional[str]=None
     )-> User:

        if email is not None:
            user.email = email
        if password is not None:
            salt, hash_password = self.create_password_hash(
                password
            )

            user.hashed_password = hash_password
            user.password_salt = salt
    
        await session.commit()
        await session.refresh(user)
        return user
    

    async def delete(self,session:AsyncSession, user:User)->User:
        await session.delete(user)
        await session.commit()


    async def get(self,session:AsyncSession, user_id: int)->Optional[User]:
        return await session.get(User, user_id)
        
    async def get_by_email(self,session:AsyncSession, email:str)->Optional[User]:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()


    async def list(self,session:AsyncSession, *,skip: int =0, limit: int = 50,) -> Iterable[User]:
        query = select(User)
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()


user = UserRepository()









