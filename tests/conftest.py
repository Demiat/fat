from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.fat.main import app


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # прямой доступ к приложению
        base_url="http://test"  # фиктивный домен для валидности URL
    ) as aclient:
        yield aclient
