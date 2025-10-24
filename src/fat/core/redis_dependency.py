"""
AsyncGenerator - абстрактный базовый класс асинхронного генератора
"""

from collections.abc import AsyncGenerator  
from contextlib import asynccontextmanager  

from redis.asyncio import ConnectionPool, Redis  

from fat.core.settings import settings  


class RedisDependency:  
    def __init__(self) -> None:  
        self._url = settings.redis_settings.redis_url  
        self._pool: ConnectionPool = self._init_pool()  

    # TODO проверить где используется кроме как здесь
    def _init_pool(self) -> ConnectionPool:  
        return ConnectionPool.from_url(
            url=self._url,
            encoding="utf-8",
            decode_responses=True
        )  

    @asynccontextmanager  
    async def get_client(self) -> AsyncGenerator:  
        redis_client = Redis(connection_pool=self._pool)  
        try:  
            yield redis_client  
        finally:  
            await redis_client.aclose()