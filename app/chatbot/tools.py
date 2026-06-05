from repositories.messages_repository import chatMessages
from repositories.session_repository import chatSession
from repositories.user_repository import user 
from models.chat_message_model import ChatMessage
from langchain_core.tools import tool

#tools de mensagens 
@tool
async def save_message(thread_id:str, role:str, content:str):
    """Salva uma mensagem no banco de dados."""
    await chatMessages.create(thread_id=thread_id, role=role, content=content)
    

@tool
async def get_messages_by_role(role:str):
    """Obtém uma mensagem pelo tipo de papel, utilize somente quando desejar alguma mensagem específica de algum tipo de role."""
    return await chatMessages.list_by_role(role=role)

@tool
async def list_messages(skip:int=0, limit:int=50):
    """Lista as mensagens com paginação."""
    return await chatMessages.list(skip=skip, limit=limit)

@tool
async def get_message(message_id:int):
    """Obtém uma mensagem específica pelo ID."""
    return await chatMessages.get(message_id=message_id)    

#tools de sessão

@tool
async def create_session(user_id:str):
    """Cria uma nova sessão de chat para um usuário específico. Apenas utilize quando for necessário criar uma nova sessão, 
    caso contrário utilize a função de update_session para atualizar o histórico da sessão já existente."""
    return await chatSession.create(
        user_id=user_id,
        thread_id=str(uuid7()),
        conversation_summary="",
        messages=[],
    )


#TODO melhorar essa rota
@tool
async def update_session(thread_id:str, message:ChatMessage):
    """Atualiza o histórico de mensagens de uma sessão existente. Utilize essa função para atualizar o histórico da sessão já existente, 
    caso contrário utilize a função de create_session para criar uma nova sessão."""
    session = await chatSession.get_by_thread(thread_id=thread_id)
    if session:
        return await chatSession.update(session, messages=message)
    return None

@tool
async def list_sessions(skip:int=0, limit:int=50):
    """Lista as sessões de chat com paginação."""
    return await chatSession.list(skip=skip, limit=limit)


#tools de usuario

@tool
async def get_user_by_email(email:str):
    """Obtém um usuário pelo email."""
    return await user.get_by_email(email=email)



TOOLS = [
    save_message,
    get_messages_by_role,
    list_messages,
    get_message,
    update_session,
    list_sessions,
    get_user_by_email,
    create_session
    
]