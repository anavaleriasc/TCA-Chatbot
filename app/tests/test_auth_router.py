import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient

@pytest.mark.asyncio
@patch("api.routes.auth_router.user.get_by_email")
@patch("api.routes.auth_router.verify_password")
@patch("api.routes.auth_router.create_access_token")
@patch("api.routes.auth_router.validate_email")
async def test_login_success(mock_validate_email, mock_create_access_token, mock_verify_password, mock_get_by_email, async_client: AsyncClient):
    # Setup mocks
    mock_validate_email.return_value = None
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "fake-token"
    
    mock_user = AsyncMock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.hashed_password = "hashed-password"
    mock_get_by_email.return_value = mock_user

    payload = {
        "email": "test@example.com",
        "password": "password123"
    }

    response = await async_client.post("/auth/login", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "fake-token"
    assert data["user"]["email"] == "test@example.com"

@pytest.mark.asyncio
@patch("api.routes.auth_router.user.get_by_email")
@patch("api.routes.auth_router.validate_email")
async def test_login_wrong_email(mock_validate_email, mock_get_by_email, async_client: AsyncClient):
    mock_validate_email.return_value = None
    mock_get_by_email.return_value = None # User not found

    payload = {
        "email": "wrong@example.com",
        "password": "password123"
    }

    response = await async_client.post("/auth/login", json=payload)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail incorreto."

@pytest.mark.asyncio
@patch("api.routes.auth_router.user.get_by_email")
@patch("api.routes.auth_router.verify_password")
@patch("api.routes.auth_router.validate_email")
async def test_login_wrong_password(mock_validate_email, mock_verify_password, mock_get_by_email, async_client: AsyncClient):
    mock_validate_email.return_value = None
    mock_verify_password.return_value = False
    
    mock_user = AsyncMock()
    mock_user.email = "test@example.com"
    mock_user.hashed_password = "hashed-password"
    mock_get_by_email.return_value = mock_user

    payload = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }

    response = await async_client.post("/auth/login", json=payload)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Senha incorreta."
