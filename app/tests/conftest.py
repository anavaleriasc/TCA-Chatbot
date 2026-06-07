import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from unittest.mock import AsyncMock

import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Set fake environment variables to bypass validation at import time
os.environ["GOOGLE_API_KEY"] = "mock_key_for_tests"
os.environ["GEMINI_API_KEY"] = "mock_key_for_tests"

from main import app
from db.database import get_db

async def override_get_db():
    # Provide a mock session. The services are mocked so they won't use it, 
    # but FastAPI dependency injection needs to be satisfied.
    yield AsyncMock()

# Override the database dependency for all tests
app.dependency_overrides[get_db] = override_get_db

import pytest_asyncio

@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
