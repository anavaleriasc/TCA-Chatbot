from models.chat_message_model import ChatMessage
from models.chat_session_model import ChatSession
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Iterable, Optional
from sqlalchemy import select



class MessagesRepository:
    async def create(self,db:AsyncSession, *, session_id:int, role: str, content: str )->ChatMessage:
        msg = ChatMessage(thread_id=session_id, role=role, content=content)
        db.add(msg)
        await db.commit()
        await db.refresh(msg)
        return msg

    async def update(self,db:AsyncSession,
     msg:ChatMessage, 
     *, 
     session_id: Optional[int]=None,
     role:Optional[str]=None, 
     content:Optional[str]=None, 
     )-> ChatMessage:

        if session_id is not None:
            msg.thread_id = session_id
        if role is not None:
            msg.role = role
        if content is not None:
            msg.content = content
    
        await db.commit()
        await db.refresh(msg)
        return msg


    async def get(self,db:AsyncSession, message_id:int)->Optional[ChatMessage]:
        return await db.get(ChatMessage, message_id)
        
    async def list_by_role(self,db:AsyncSession, role:str)->Optional[ChatMessage]:
        query = select(ChatMessage).where(ChatMessage.role == role)
        result = await db.execute(query)
        return result.scalars().all()

    async def list_by_thread(self, db: AsyncSession, thread_id: str) -> Iterable[ChatMessage]:
        # Busca diretamente as mensagens onde o thread_id seja igual ao passado
        query = select(ChatMessage).where(ChatMessage.thread_id == thread_id)
        result = await db.execute(query)
        
        # Retorna a lista de mensagens (se não tiver nenhuma, ele já retorna vazio automaticamente)
        return result.scalars().all()


    async def list(self,db:AsyncSession, *,skip: int =0, limit: int = 50,) -> Iterable[ChatMessage]:
        query = select(ChatMessage)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()


chatMessages = MessagesRepository()









