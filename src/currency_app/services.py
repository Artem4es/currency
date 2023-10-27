import logging
from http import HTTPStatus

from fastapi import HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from src.currency_app.crud import (
    get_db_currency_rates,
    update_db_currency_names,
    update_db_currency_rates,
)
from src.currency_app.schemas import ConvertResponse, CurrencyCodes, GetCodes, GetRates

logger = logging.getLogger(__name__)

settings = Settings()


def fill_currency_codes_class(codes: dict) -> None:
    """Add code attributes to CurrencyCodes class"""
    for code, description in codes.items():
        setattr(CurrencyCodes, code, description)

############################
async def get_currency_data(client: AsyncClient) -> dict:
    """Get currency names, codes and rats"""
    symbols: GetCodes = await get_currency_names(client)
    rates: GetRates = await get_currency_rates(client)
    fill_currency_codes_class(symbols.codes)
    return dict(symbols=symbols, rates=rates)

async def update_currency(client: AsyncClient, db_session: AsyncSession) -> None:
    """Update all currency data in DB"""
    logger.info("Refresh DB data has started ...")
    # symbols: GetCodes = await get_currency_names(client)
    # await update_db_currency_names(db_session, symbols.codes)
    #
    # # fill_currency_codes_class(symbols.codes)
    #
    # # rates: GetRates = await get_currency_rates(client)
    # await update_db_currency_rates(db_session, rates)
    # logger.info("Refresh DB data has been successfully finished")


async def get_currency_names(client: AsyncClient) -> GetCodes:
    """Get currency names and codes from external API"""
    access_key = {"access_key": settings.api_key}
    resp = await client.get(url=settings.currency_names, params=access_key)
    if resp.status_code == HTTPStatus.OK:
        res: dict = resp.json()
        codes_data = GetCodes(success=res["success"], codes=res["symbols"])
        return codes_data

    else:
        logger.error(f"Ответ API != 200: {resp.status_code} | {resp.json()}")
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Couldn't get response from external API")


async def get_currency_rates(client: AsyncClient) -> GetRates:
    """Get currency rates from external API"""
    access_key = {"access_key": settings.api_key}
    resp = await client.get(url=settings.currency_rates, params=access_key)
    if resp.status_code == HTTPStatus.OK:
        res = resp.json()
        rates = GetRates(**res)
        return rates

    else:
        logger.error(f"Ответ API != 200: {resp.status_code} | {resp.json()}")
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Couldn't get response from external API")


async def calculate_amount(db_session: AsyncSession, from_curr: str, to_curr: str, from_curr_amount: float) -> ConvertResponse:
    """Calculate amount of 'to_curr' currency based on DB exchange rate"""
    curr_rates: dict = await get_db_currency_rates(db_session, from_curr, to_curr)

    from_curr_rate = curr_rates["from_curr_rate"]
    to_curr_rate = curr_rates["to_curr_rate"]
    last_updated = curr_rates["last_updated"]
    to_curr_amount: float = from_curr_amount * (to_curr_rate / from_curr_rate)
    return ConvertResponse(
        from_currency=from_curr, to_currency=to_curr, amount=from_curr_amount, result=to_curr_amount, last_updated=last_updated
    )
