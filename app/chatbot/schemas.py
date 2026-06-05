from pydantic import BaseModel


class ChatResponse(BaseModel):
    interaction_type: str
    model: str
    message: str
    thread_id: str

class ChatRequest(BaseModel):
    user_id: int
    thread_id: str
    message: str