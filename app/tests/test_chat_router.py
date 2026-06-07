import pytest
from unittest.mock import patch
from httpx import AsyncClient

@pytest.mark.asyncio
@patch("api.routes.chat_router.send_message")
async def test_invoke_chat(mock_send_message, async_client: AsyncClient):
    # Setup mock
    mock_send_message.return_value = {
        "interaction_type": "chat",
        "model": "gemini",
        "message": "Hello, how can I help you?",
        "thread_id": "thread-123"
    }

    payload = {
        "user_id": 1,
        "message": "Hi",
        "thread_id": "thread-123"
    }

    response = await async_client.post("/chat/invoke", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, how can I help you?"
    assert data["thread_id"] == "thread-123"
