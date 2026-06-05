from models.chat_session_model import ChatSession
from models.chat_message_model import ChatMessage
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Iterable, Optional
from sqlalchemy import select


class SessionRepository:
    async def create(self,db:AsyncSession, *, thread_id: str, user_id:str, conversation_summary:str, messages:ChatMessage )->ChatSession:
        session = ChatSession(thread_id=thread_id, user_id=user_id, conversation_summary=conversation_summary, messages=messages)
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    async def update(self,db:AsyncSession,
     session:ChatSession, 
     *, 
     thread_id: Optional[str]=None,
     user_id:Optional[str]=None, 
     conversation_summary:Optional[str]=None, 
     messages:Optional[ChatMessage]=None
     )-> ChatSession:

        if thread_id is not None:
            session.thread_id = thread_id
        if user_id is not None:
            session.user_id = user_id
        if conversation_summary is not None:
            session.conversation_summary = conversation_summary
        if messages is not None:
            session.messages = messages
    
        await db.commit()
        await db.refresh(session)
        return session


    async def get(self,db:AsyncSession, session_id:int)->Optional[ChatSession]:
        return await db.get(ChatSession, session_id)
        
    async def get_by_thread(self,db:AsyncSession, thread_id:str)->Optional[ChatSession]:
        query = select(ChatSession).where(ChatSession.thread_id == thread_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()


    async def list(self,db:AsyncSession, *,skip: int =0, limit: int = 50,) -> Iterable[ChatSession]:
        query = select(ChatSession)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()


chatSession = SessionRepository()









