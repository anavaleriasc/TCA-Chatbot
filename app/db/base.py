from sqlalchemy.orm import DeclarativeBase
import sys
import os

class Base(DeclarativeBase):
    pass

# Importa modelos para o Alembic registrar as tabelas
try:
    # Tenta importar como se estivéssemos na raiz (Alembic)
    from models import user_model, chat_session_model, chat_message_model
except ImportError:
    # Caso falhe, tenta importar a partir do diretório atual (Uvicorn)
    from app.models import user_model, chat_session_model, chat_message_model