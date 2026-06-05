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

    async def list_by_thread(self,db:AsyncSession, thread_id:str)->Iterable[ChatMessage]:
        session_query = select(ChatSession).where(ChatSession.thread_id == thread_id)
        session_result = await db.execute(session_query)
        session = session_result.scalars().all()
        
        if not session:
            return []
        
        query = select(ChatMessage).where(ChatMessage.thread_id == session.thread_id)
        result = await db.execute(query)
        return result.scalars().all()


    async def list(self,db:AsyncSession, *,skip: int =0, limit: int = 50,) -> Iterable[ChatMessage]:
        query = select(ChatMessage)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()


chatMessages = MessagesRepository()









