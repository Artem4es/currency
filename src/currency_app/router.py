from fastapi import APIRouter, Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from src.currency_app.crud import update_db_rates
from src.currency_app.dependencies import get_async_client
from src.currency_app.service import get_currency_rates

router = APIRouter()


@router.get("/update_rates")
async def update_rates(db_session: AsyncSession = Depends(get_async_session), client: AsyncClient =Depends(get_async_client)):
    """Update rates for all or given??? currency???"""
    rates = await get_currency_rates(client)
    await update_db_rates(db_session, rates)


@router.get("/last_update")
async def last_update():
    """Get last update time for for all or given??? currency???"""


@router.get("/convert/")
async def convert(first: str, second: str, amount: float | int):
    """Calculates amount of second currency based on currency rate"""
