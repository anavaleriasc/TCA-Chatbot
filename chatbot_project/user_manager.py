import hashlib
import hmac
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional

# guarda os usuários usando o email como chave 
_users_by_email: Dict[str, Dict[str, str]] = {}

# ajusta o formato do email
def _normalize_email(email: str) -> str:
    return email.strip().lower()

# gera um hash usando hmac para evitar salvar a senha em claro
def _hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    salt = salt or os.urandom(16).hex()
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        100_000,
    ).hex()
    return salt, password_hash


'''
cria um novo usuário:
- verifica se o email já existe
- gera um salt e hash para a senha
- armazena o usuário no dicionário
- salva nome, email, id e data de criação
'''
def create_user(name: str, email: str, password: str) -> Dict[str, str]:
    normalized_email = _normalize_email(email)
    if normalized_email in _users_by_email:
        raise ValueError("E-mail ja cadastrado.")

    salt, password_hash = _hash_password(password)
    user = {
        "id": str(uuid.uuid4()),
        "name": name.strip(),
        "email": normalized_email,
        "password_salt": salt,
        "password_hash": password_hash,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _users_by_email[normalized_email] = user
    return get_public_user(normalized_email)

'''
Autenticação do usuário:
- busca o email;
- se o email existir, gera o hash da senha fornecida usando o salt armazenado;
- compara o hash gerado com o hash armazenado usando hmac.compare_digest para evitar ataques de timing;
- se a autenticação for bem-sucedida, retorna os dados públicos do usuário.
'''
def authenticate_user(email: str, password: str) -> Optional[Dict[str, str]]:
    user = _users_by_email.get(_normalize_email(email))
    if not user:
        return None

    _, password_hash = _hash_password(password, user["password_salt"])
    if not hmac.compare_digest(password_hash, user["password_hash"]):
        return None

    return get_public_user(email)

# retorna apenas os campos públicos do usuário
def get_public_user(email: str) -> Optional[Dict[str, str]]:
    user = _users_by_email.get(_normalize_email(email))
    if not user:
        return None

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"],
    }
