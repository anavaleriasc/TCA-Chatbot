from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class SessionPublic(BaseModel):
    thread_id: Optional[str] = None
    conversation_summary:Optional[str] = None
    created_at:Optional[datetime] = None
    updated_at:Optional[datetime] = None

    class Config:
        from_attributes=True



