import hashlib
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional


_users_by_email: Dict[str, Dict[str, str]] = {}


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    salt = salt or os.urandom(16).hex()
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        100_000,
    ).hex()
    return salt, password_hash


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
    return user


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
