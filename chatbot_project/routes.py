from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from session_manager import create_session, get_history, add_message
from llm_service import generate_chat_response

router = APIRouter()

# Schema (Modelo) que define a estrutura do JSON recebido do frontend
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

# Schema que define a estrutura do JSON enviado de volta ao frontend
class ChatResponse(BaseModel):
    session_id: str
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Se o usuário é novo e não enviou um session_id, criamos um
    session_id = request.session_id
    if not session_id:
        session_id = create_session()
    
    user_msg = request.message
    
    # Resgata o histórico isolado do usuário com base no seu session_id
    # Se for uma sessão nova, isso retorna uma lista vazia []
    history = get_history(session_id)
    
    # Chama o LLM passando o histórico da sessão e a nova mensagem
    bot_response = generate_chat_response(history, user_msg)
    
    # Salva as duas mensagens (a do user e a do bot) no histórico de memória
    add_message(session_id, "user", user_msg)
    add_message(session_id, "model", bot_response)
    
    # Retorna para o frontend o texto e o session_id gerado (ou mantido)
    return ChatResponse(session_id=session_id, response=bot_response)
