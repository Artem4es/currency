from http import HTTPStatus

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.currency_app.crud import update_db_currency_names, update_db_currency_rates
from src.currency_app.schema import GetRates, GetCodes
from config import Settings
import logging

logger = logging.getLogger(__name__)

settings = Settings()


async def update_currency_table(client: AsyncClient, db_session: AsyncSession) -> None:
    """Update all currency data in DB"""
    symbols: dict = await get_currency_names(client)
    await update_db_currency_names(db_session, symbols)

    rates: GetRates = await get_currency_rates(client)
    await update_db_currency_rates(db_session, rates)


async def get_currency_names(client: AsyncClient) -> dict:
    """Get currency names and codes from external API"""
    access_key = {"access_key": settings.api_key}
    resp = await client.get(url=settings.currency_names, params=access_key)
    if resp.status_code == HTTPStatus.OK:
        res: dict = resp.json()
        codes = GetCodes(**res)
        return codes.symbols

    else:
        logger.error(f"Ответ API != 200: {resp.status_code | resp.json()}")
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Не удалось получить ответ от внешнего сервиса")


async def get_currency_rates(client: AsyncClient) -> GetRates:
    """Get currency rates from external API"""
    access_key = {"access_key": settings.api_key}
    resp = await client.get(url=settings.currency_rates, params=access_key)
    if resp.status_code == HTTPStatus.OK:
        res = resp.json()
        rates = GetRates(**res)
        return rates

    else:
        logger.error(f"Ответ API != 200: {resp.status_code | resp.json()}")
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Не удалось получить ответ от внешнего сервиса")



