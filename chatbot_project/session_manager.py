import uuid
from typing import Dict, List, Any

# Armazena em memória as sessões ativas e seus históricos
# Formato: { "session_id": [ {"role": "user", "parts": ["hello"]}, {"role": "model", "parts": ["hi"]} ] }
_sessions: Dict[str, List[Dict[str, Any]]] = {}

def create_session() -> str:
    """Cria um novo ID de sessão usando UUID e inicializa o histórico vazio."""
    session_id = str(uuid.uuid4())
    _sessions[session_id] = []
    return session_id

def get_history(session_id: str) -> List[Dict[str, Any]]:
    """Retorna o histórico de uma sessão. Retorna lista vazia se não existir."""
    return _sessions.get(session_id, [])

def add_message(session_id: str, role: str, content: str):
    """
    Adiciona uma mensagem ao histórico da sessão. 
    O 'role' deve ser 'user' ou 'model' (padrão exigido pelo Google Generative AI).
    """
    if session_id not in _sessions:
        _sessions[session_id] = []
    
    _sessions[session_id].append({
        "role": role,
        "parts": [content]
    })
