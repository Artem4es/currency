from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import get_async_session
from src.currency_app.dependencies import get_async_client
from src.currency_app.service import update_currency


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Update currency data in DB on app startup"""

    async for client in get_async_client():
        async for db_session in get_async_session():
            await update_currency(client, db_session)
    yield