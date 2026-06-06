from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MessagePublic(BaseModel):
    id: Optional[int] = None
    thread_id: Optional[str] = None
    role:Optional[str] = None
    created_at:Optional[datetime] = None
    content:Optional[str] = None

    class Config:
        from_attributes=True
