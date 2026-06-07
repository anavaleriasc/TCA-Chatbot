import os
import re
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from typing import Optional
from session_manager import create_session, get_history, add_message
from llm_service import generate_chat_response
from user_manager import authenticate_user, create_user, get_public_user

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

router = APIRouter()
bearer_scheme = HTTPBearer()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise RuntimeError("Configure JWT_SECRET_KEY no arquivo .env ou nas variaveis de ambiente.")

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60



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
