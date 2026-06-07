import pytest
from unittest.mock import patch
from httpx import AsyncClient

# Models for mocking responses
from schemas.messages_schema import MessagePublic

@pytest.mark.asyncio
@patch("api.routes.messages_router.listar_mensagens")
async def test_list_messages(mock_listar_mensagens, async_client: AsyncClient):
    # Setup mock
    mock_listar_mensagens.return_value = [
        MessagePublic(id=1, thread_id="thread-1", role="user", content="Hello"),
        MessagePublic(id=2, thread_id="thread-1", role="bot", content="Hi")
    ]

    response = await async_client.get("/mensagens")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["role"] == "user"
    assert data[1]["content"] == "Hi"

@pytest.mark.asyncio
@patch("api.routes.messages_router.listar_mensagem_by_thread")
async def test_list_message_by_thread(mock_listar_mensagem_by_thread, async_client: AsyncClient):
    # Setup mock
    mock_listar_mensagem_by_thread.return_value = [
        MessagePublic(id=1, thread_id="thread-1", role="user", content="Hello")
    ]

    response = await async_client.get("/mensagens/thread-1")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["thread_id"] == "thread-1"
    assert data[0]["role"] == "user"
