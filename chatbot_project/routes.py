import os
import re
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from typing import Optional
from session_manager import create_session, get_history, add_message
from llm_service import generate_chat_response
from user_manager import authenticate_user, create_user, get_public_user

router = APIRouter()
bearer_scheme = HTTPBearer()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "troque-esta-chave-secreta-em-producao-32")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60

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
    access_token: str
    token_type: str
    user: UserResponse

def _create_access_token(user: dict) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        "sub": user["email"],
        "user_id": user["id"],
        "name": user["name"],
        "exp": expires_at,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError as error:
        raise HTTPException(status_code=401, detail="Token expirado.") from error
    except jwt.InvalidTokenError as error:
        raise HTTPException(status_code=401, detail="Token invalido.") from error

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token invalido.")

    user = get_public_user(email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario nao encontrado.")

    return user

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

    access_token = _create_access_token(user)
    return AuthResponse(
        message="Cadastro criado com sucesso.",
        access_token=access_token,
        token_type="bearer",
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

    access_token = _create_access_token(user)
    return AuthResponse(
        message="Login realizado com sucesso.",
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(id=user["id"], name=user["name"], email=user["email"]),
    )

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, current_user: dict = Depends(get_current_user)):
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
