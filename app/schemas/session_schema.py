from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from schemas.messages_schema import MessagePublic as ChatMessage





class SessionCreate(BaseModel):
    thread_id: str
    user_id: str
    conversation_summary: Optional[str] = None
    messages: Optional[ChatMessage] = None

class SessionUpdate(BaseModel):
    thread_id: Optional[str] = None
    user_id: Optional[str] = None
    conversation_summary: Optional[str] = None
    messages: Optional[ChatMessage] = None



class SessionPublic(BaseModel):
    thread_id: Optional[str] = None
    conversation_summary:Optional[str] = None
    created_at:Optional[datetime] = None
    updated_at:Optional[datetime] = None



class Config:
        from_attributes=True






