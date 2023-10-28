import logging
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from src.currency_app.crud import get_db_time_update, update_db_currency_rates
from src.currency_app.dependencies import get_async_client
from src.currency_app.managers import update_manager
from src.currency_app.models import UpdateTimeDB
from src.currency_app.responses import convert_resp, last_update_resp, update_rates_resp
from src.currency_app.schemas import (
    ConvertResponse,
    GetRates,
    TimeDateResponse,
    UpdateRatesResponse,
    UpdateRespStatus,
)
from src.currency_app.services import calculate_amount, get_currency_rates
from src.currency_app.validators import (
    validate_curr_amount,
    validate_from_curr,
    validate_to_curr,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/update_rates", responses=update_rates_resp)
async def update_rates(
    db_session: AsyncSession = Depends(get_async_session), client: AsyncClient = Depends(get_async_client)
) -> UpdateRatesResponse:
    """Update rates info for all currencies"""
    if not update_manager.has_expired():
        expires_in: int = update_manager.expires_in()
        raise HTTPException(
            status_code=HTTPStatus.TOO_EARLY, detail=f"Rates are still fresh. Update in {expires_in} seconds, please!"
        )

    rates_resp: GetRates = await get_currency_rates(client)
    update_time_data: UpdateTimeDB = await update_db_currency_rates(db_session, rates_resp)

    logger.info("DB rates were updated by user request via /update_rates")
    return UpdateRatesResponse(
        status=UpdateRespStatus.SUCCESS, update_time=update_time_data.updated_timestamp, update_date=update_time_data.updated_date
    )


@router.get("/last_update", responses=last_update_resp)
async def last_update(db_session: AsyncSession = Depends(get_async_session)) -> TimeDateResponse:
    """Get last update time for currency rates from DB"""
    timedate: Optional[TimeDateResponse] = await get_db_time_update(db_session)
    if timedate:
        return timedate

    raise HTTPException(status_code=HTTPStatus.TOO_EARLY, detail={"detail": "No data in DB, please update rates"})


@router.get("/convert", responses=convert_resp)
async def convert(
    from_curr_amount: float = Depends(validate_curr_amount),
    from_curr: str = Depends(validate_from_curr),
    to_curr: str = Depends(validate_to_curr),
    db_session: AsyncSession = Depends(get_async_session),
) -> ConvertResponse:
    """Calculates amount of 'to_curr' currency based on currency rate from DB"""
    conversion_data: ConvertResponse = await calculate_amount(db_session, from_curr, to_curr, from_curr_amount)
    return conversion_data
