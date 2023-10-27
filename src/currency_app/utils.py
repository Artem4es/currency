import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import AsyncClient
from database import get_async_session, async_session_maker
from src.currency_app.crud import update_db_currency_names, update_db_currency_rates
from src.currency_app.dependencies import get_async_client
from src.currency_app.schemas import GetCodes, GetRates
from src.currency_app.services import update_currency, get_currency_data
from config import Settings

settings = Settings()
logger = logging.getLogger(__name__)
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Update currency data in DB on app startup"""
#
#     async for client in get_async_client():
#         async for db_session in get_async_session():
#             await update_currency(client, db_session)
#     yield


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Update currency data in DB on app startup"""

    async with AsyncClient(base_url=settings.base_currency_url) as client:
        logger.info("Refresh DB data has started ...")
        currency_data: dict = await get_currency_data(client)

        symbols: GetCodes = currency_data["symbols"]
        rates: GetRates = currency_data["rates"]

    async with async_session_maker() as db_session:
        await update_db_currency_names(db_session, symbols.codes)
        await update_db_currency_rates(db_session, rates)
        logger.info("Refresh DB data has been successfully finished")
        # await update_currency(client, db_session)
    yield