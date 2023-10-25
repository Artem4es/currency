from datetime import datetime

from pydantic import condate
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_app.model import CurrencyDB
from src.currency_app.schema import GetRates


# from src.currency_app.schema import Symbols, Rates


# async def get_db_currency_items(db_session: AsyncSession) -> list[CurrencyDB]:
#     stmt = select(CurrencyDB)
#     res = await db_session.execute(stmt)
#     return list(res.scalars())

async def update_db_currency_names(db_session: AsyncSession, symbols: dict) -> None:
    """Fill in DB with currency names and codes"""
    for code, name in symbols.items():                      # bulk не получится?
        currency_item = CurrencyDB(name=name, code=code)
        await db_session.merge(currency_item)   #  add_all()???

    await db_session.commit()


async def update_db_currency_rates(db_session: AsyncSession, rates_resp: GetRates) -> None:
    """Update currency rates in DB"""
    date: condate = rates_resp.date
    timestamp: int = rates_resp.timestamp
    rates = rates_resp.rates
    for code, rate in rates.items():
        stmt = update(CurrencyDB).where(CurrencyDB.code == str(code)).values(rate=rate, updated_date=date, updated_timestamp=timestamp)  # Проверить и нужен ли str?
        await db_session.execute(stmt)

    await db_session.commit()

