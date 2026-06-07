import pytest
from unittest.mock import patch
from httpx import AsyncClient

# Models for mocking responses
from schemas.session_schema import SessionPublic

@pytest.mark.asyncio
@patch("api.routes.session_router.listar_sessoes")
async def test_list_sessions(mock_listar_sessoes, async_client: AsyncClient):
    # Setup mock
    mock_listar_sessoes.return_value = [
        SessionPublic(thread_id="thread-1", conversation_summary="Summary 1"),
        SessionPublic(thread_id="thread-2", conversation_summary="Summary 2")
    ]

    response = await async_client.get("/sessoes")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["thread_id"] == "thread-1"
    assert data[1]["conversation_summary"] == "Summary 2"

@pytest.mark.asyncio
@patch("api.routes.session_router.get_sessao_by_thread")
async def test_get_sessions_by_thread(mock_get_sessao_by_thread, async_client: AsyncClient):
    # Setup mock
    mock_get_sessao_by_thread.return_value = SessionPublic(thread_id="thread-1", conversation_summary="Summary 1")

    response = await async_client.get("/sessoes/thread-1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["thread_id"] == "thread-1"
    assert data["conversation_summary"] == "Summary 1"
