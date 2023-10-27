import logging

from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.currency_app.crud import update_db_currency_rates, get_time_update
from src.currency_app.dependencies import get_async_client
from src.currency_app.validators import validate_from_curr, validate_to_curr, validate_curr_amount
from src.currency_app.model import UpdateTimeDB
from src.currency_app.responses import no_db_data, bad_ext_api_resp, convert_bad_responses
from src.currency_app.schema import GetRates, UpdateRatesResponse, UpdateRespStatus, TimeDateResponse, ConvertResponse

from src.currency_app.service import get_currency_rates
from src.currency_app.service import calculate_amount

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/update_rates", responses=bad_ext_api_resp)
async def update_rates(db_session: AsyncSession = Depends(get_async_session), client: AsyncClient = Depends(get_async_client)) -> UpdateRatesResponse:
    """Update rates info for all currencies"""
    rates_resp: GetRates = await get_currency_rates(client)
    update_time_data: UpdateTimeDB = await update_db_currency_rates(db_session, rates_resp)

    logger.info("DB rates were updated by user request via /update_rates")
    return UpdateRatesResponse(status=UpdateRespStatus.SUCCESS, update_time=update_time_data.updated_timestamp, update_date=update_time_data.updated_date)


@router.get("/last_update", responses=no_db_data)
async def last_update(db_session: AsyncSession = Depends(get_async_session)) -> TimeDateResponse:
    """Get last update time for currency rates"""
    timedate: Optional[TimeDateResponse] = await get_time_update(db_session)
    if timedate:
        return timedate

    raise HTTPException(status_code=HTTPStatus.TOO_EARLY, detail={"detail": "No data in DB, please update rates"})


# @router.get("/convert")   # так можно но нет доки...
# async def convert(from_curr: CurrencyCode, to_curr: CurrencyCode, from_curr_amount: float = Query(description="Any positive number. Dot should be used as separator: 1.556)", gt=0), db_session: AsyncSession = Depends(get_async_session)) -> ConvertResponse:
#     """Calculates amount of second currency based on currency rate"""
#     curr_rates: dict = await calculate_amount(db_session, from_curr, to_curr, from_curr_amount)
#     response = ConvertResponse(from_currency=from_curr, to_currency=to_curr, amount=from_curr_amount, result=curr_rates["result"], last_updated=curr_rates["last_updated"])
#     return response


@router.get("/convert", responses=convert_bad_responses)
async def convert(from_curr_amount: float = Depends(validate_curr_amount), from_curr: str = Depends(validate_from_curr), to_curr: str = Depends(validate_to_curr), db_session: AsyncSession = Depends(get_async_session)) -> ConvertResponse:
    """Calculates amount of 'to_curr' currency based on currency rate from DB"""
    conversion_data: ConvertResponse = await calculate_amount(db_session, from_curr, to_curr, from_curr_amount)
    return conversion_data
