from typing import AsyncGenerator

from httpx import AsyncClient

# from currency.config import Settings
from config import Settings

settings = Settings()


async def get_async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(base_url=settings.base_currency_url) as client:
        yield client
