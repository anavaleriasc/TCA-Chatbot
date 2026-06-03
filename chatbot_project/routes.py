import re

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from session_manager import create_session, get_history, add_message
from llm_service import generate_chat_response
from user_manager import authenticate_user, create_user

router = APIRouter()

# Schema (Modelo) que define a estrutura do JSON recebido do frontend
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

# Schema que define a estrutura do JSON enviado de volta ao frontend
class ChatResponse(BaseModel):
    session_id: str
    response: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

class AuthResponse(BaseModel):
    message: str
    user: UserResponse

def _validate_email(email: str):
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()):
        raise HTTPException(status_code=400, detail="Informe um e-mail valido.")

def _validate_registration(request: RegisterRequest):
    if len(request.name.strip()) < 2:
        raise HTTPException(status_code=400, detail="Informe um nome com pelo menos 2 caracteres.")

    _validate_email(request.email)

    if len(request.password) < 6:
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 6 caracteres.")

@router.post("/register", response_model=AuthResponse, status_code=201)
async def register_endpoint(request: RegisterRequest):
    _validate_registration(request)

    try:
        user = create_user(request.name, request.email, request.password)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error

    return AuthResponse(
        message="Cadastro criado com sucesso.",
        user=UserResponse(id=user["id"], name=user["name"], email=user["email"]),
    )

@router.post("/login", response_model=AuthResponse)
async def login_endpoint(request: LoginRequest):
    _validate_email(request.email)

    if not request.password:
        raise HTTPException(status_code=400, detail="Informe sua senha.")

    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

    return AuthResponse(
        message="Login realizado com sucesso.",
        user=UserResponse(id=user["id"], name=user["name"], email=user["email"]),
    )

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
