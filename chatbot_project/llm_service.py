import os
from google import genai
from typing import List, Dict, Any
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Tenta carregar a chave da variável de ambiente
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# 1. Inicializa o Client do novo SDK uma única vez aqui fora (substitui o genai.configure)
client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None

def generate_chat_response(history: List[Dict[str, Any]], new_message: str) -> str:
    """
    Continua uma conversa com o Gemini 1.5 Flash, considerando o histórico isolado do usuário.
    """
    if not client:
        return "Erro de Servidor: A variável de ambiente GOOGLE_API_KEY não foi configurada."

    try:
        # 2. Garante que o histórico esteja no formato exato que o novo SDK exige
        contents = []
        for msg in history:
            role = msg.get("role")
            parts = msg.get("parts", [])
            
            # Lida com segurança tanto com o formato antigo ["texto"] quanto o novo [{"text": "texto"}]
            if len(parts) > 0:
                text_content = parts[0] if isinstance(parts[0], str) else parts[0].get("text", "")
                contents.append({"role": role, "parts": [{"text": text_content}]})
        
        # 3. Adiciona a nova mensagem do usuário à lista de contexto
        contents.append({"role": "user", "parts": [{"text": new_message}]})
        
        # 4. Gera a resposta usando o client e o formato atualizado
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents
        )
        
        return response.text
    except Exception as e:
        return f"Ocorreu um erro ao processar a mensagem: {str(e)}"