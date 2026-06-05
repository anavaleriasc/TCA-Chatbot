from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from repositories.session_repository import chatSession
from chatbot.tools import TOOLS
from repositories.messages_repository import chatMessages
from repositories.user_repository import user
from chatbot.schemas import ChatRequest, ChatResponse
from typing import List
from chatbot.prompt import SYSTEM_PROMPT
from chatbot.agent import get_agent


llm = get_agent()
print(llm)

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])


chain = prompt | llm | StrOutputParser()


def _build_langchain_history(db_messages: list) -> List[HumanMessage | AIMessage]:
    lc_history: List[HumanMessage | AIMessage] = []
    for msg in db_messages:
        if msg.role == "user":
            lc_history.append(HumanMessage(content=msg.content))
        elif msg.role in ("bot", "assistant", "ai"):
            lc_history.append(AIMessage(content=msg.content))
    return lc_history


async def send_message(
    session: AsyncSession,
    payload: ChatRequest,
):
    user_data = await user.get(session=session, user_id=payload.user_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    session_data = await chatSession.get_by_thread(
        db=session, thread_id=payload.thread_id
    )
    if not session_data:
        session_data = await chatSession.create(
            db=session,
            user_id=payload.user_id,
            thread_id=payload.thread_id,
            conversation_summary="",
            messages=[],
        )

    # Salva a mensagem do usuário
    await chatMessages.create(
        db=session,
        session_id=session_data.id,
        role="user",
        content=payload.message,
    )

    db_history = await chatMessages.list_by_thread(
        db=session, thread_id=payload.thread_id
    )
    lc_history = _build_langchain_history(db_history)

  
    try:
        chatbot_response: str = await chain.ainvoke({
            "input": payload.message,
            "history": lc_history,  
        })
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro ao chamar o modelo de linguagem: {exc}",
        )


    await chatMessages.create(
        db=session,
        session_id=session_data.id,
        role="bot",
        content=chatbot_response,
    )

    return ChatResponse(
        interaction_type="response",
        model=llm.model,
        message=chatbot_response,
        thread_id=payload.thread_id,
    )