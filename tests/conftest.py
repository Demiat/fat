from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.fat.main import app


# Конфигурация всех эндпоинтов проекта
class Endpoints:
    """Константы всех эндпоинтов API"""

    # Auth endpoints
    AUTH_REGISTER = "/api/v1/auth/register"
    AUTH_REGISTER_CONFIRM = "/api/v1/auth/register_confirm"
    AUTH_LOGIN = "/api/v1/auth/login"
    AUTH_LOGOUT = "/api/v1/auth/logout"
    AUTH_GET_USER = "/api/v1/auth/get-user"

    # Common endpoints
    ROOT = "/"
    DOCS = "/docs"
    OPENAPI = "/openapi.json"
    HEALTH = "/health"


@pytest_asyncio.fixture(scope="session")
def endpoints():
    """Фикстура с константами эндпоинтов"""
    return Endpoints


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # прямой доступ к приложению
        base_url="http://test"  # фиктивный домен для валидности URL
    ) as aclient:
        yield aclient
