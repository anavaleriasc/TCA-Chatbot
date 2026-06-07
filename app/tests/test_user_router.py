import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient

# Models for mocking responses
from schemas.user_schema import UserPublic, AuthResponse

@pytest.mark.asyncio
@patch("api.routes.user_router.adicionar_usuario")
@patch("api.routes.user_router.create_access_token")
async def test_create_user(mock_create_access_token, mock_adicionar_usuario, async_client: AsyncClient):
    # Setup mocks
    mock_user = AsyncMock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_adicionar_usuario.return_value = mock_user
    mock_create_access_token.return_value = "fake-token"

    payload = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }

    response = await async_client.post("/usuarios", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["access_token"] == "fake-token"
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["id"] == 1

@pytest.mark.asyncio
@patch("api.routes.user_router.listar_usuarios")
async def test_list_users(mock_listar_usuarios, async_client: AsyncClient):
    # Setup mocks
    mock_listar_usuarios.return_value = [
        UserPublic(id=1, email="test1@example.com"),
        UserPublic(id=2, email="test2@example.com")
    ]

    response = await async_client.get("/usuarios")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == "test1@example.com"

@pytest.mark.asyncio
@patch("api.routes.user_router.get_usuario")
async def test_get_user(mock_get_usuario, async_client: AsyncClient):
    # Setup mocks
    mock_get_usuario.return_value = UserPublic(id=1, email="test@example.com")

    response = await async_client.get("/usuarios/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["email"] == "test@example.com"

@pytest.mark.asyncio
@patch("api.routes.user_router.atualizar_usuario")
async def test_update_user(mock_atualizar_usuario, async_client: AsyncClient):
    # Setup mocks
    mock_atualizar_usuario.return_value = UserPublic(id=1, email="updated@example.com")

    payload = {"email": "updated@example.com"}

    response = await async_client.patch("/usuarios/1", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"

@pytest.mark.asyncio
@patch("api.routes.user_router.remover_usuario")
async def test_delete_user(mock_remover_usuario, async_client: AsyncClient):
    # Setup mocks
    mock_remover_usuario.return_value = UserPublic(id=1, email="test@example.com")

    response = await async_client.delete("/usuarios/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
