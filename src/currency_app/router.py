from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from src.currency_app.crud import update_db_currency_rates, get_time_update, update_currency_dates
from src.currency_app.dependencies import get_async_client
from src.currency_app.model import UpdateTimeDB
from src.currency_app.schema import GetRates, UpdateRatesResponse, UpdateRespStatus, TimeDateResponse, ConvertResponse
from src.currency_app.service import get_currency_rates
from src.currency_app.utils import calculate_amount

router = APIRouter()


@router.get("/update_rates")
async def update_rates(db_session: AsyncSession = Depends(get_async_session), client: AsyncClient = Depends(get_async_client)) -> UpdateRatesResponse:
    """Update rates info for all currencies"""
    rates_resp: GetRates = await get_currency_rates(client)
    update_time_data: UpdateTimeDB = await update_db_currency_rates(db_session, rates_resp)

    return UpdateRatesResponse(status=UpdateRespStatus.SUCCESS, update_time=update_time_data.updated_timestamp, update_date=update_time_data.updated_date)


@router.get("/last_update")
async def last_update(db_session: AsyncSession = Depends(get_async_session)) -> TimeDateResponse:
    """Get last update time for currency rates"""
    timedate: Optional[TimeDateResponse] = await get_time_update(db_session)
    if timedate:
        return timedate

    raise HTTPException(status_code=HTTPStatus.NO_CONTENT, detail={"detail": "No data in DB, please update rates"})


@router.get("/convert")
async def convert(from_curr: str, to_curr: str, from_curr_amount: float, db_session: AsyncSession = Depends(get_async_session)) -> ConvertResponse:
    """Calculates amount of second currency based on currency rate"""
    curr_rates: dict = await calculate_amount(db_session, from_curr, to_curr, from_curr_amount)
    response = ConvertResponse(from_currency=from_curr, to_currency=to_curr, amount_from=from_curr_amount, result=curr_rates["result"], last_updated=curr_rates["last_updated"])
    return response
