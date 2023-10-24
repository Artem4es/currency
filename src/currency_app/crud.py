from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_app.schema import CurrencyUpdate


async def update_db_rates(db_session: AsyncSession, rates: list[CurrencyUpdate]) -> None:
    """Update currency rates in DB"""
