from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_app.models import CurrencyDB, UpdateTimeDB
from src.currency_app.schemas import GetRates, TimeDateResponse


async def update_db_currency_names(db_session: AsyncSession, symbols: dict) -> None:
    """Fill in DB with currency names and codes"""
    for code, name in symbols.items():
        currency_item = CurrencyDB(name=name, code=code)
        await db_session.merge(currency_item)

    await db_session.commit()


async def update_db_currency_rates(db_session: AsyncSession, rates_resp: GetRates) -> UpdateTimeDB:
    """Update currency rates in DB"""
    update_time_data: UpdateTimeDB = await update_currency_dates(db_session, rates_resp)
    rates = rates_resp.rates
    for code, rate in rates.items():
        stmt = update(CurrencyDB).where(CurrencyDB.code == code).values(rate=rate, updatetime_id=update_time_data.id)
        await db_session.execute(stmt)

    await db_session.commit()
    return update_time_data


async def update_currency_dates(db_session: AsyncSession, rates_resp: GetRates) -> UpdateTimeDB:
    """Update currency date of update (at external API)"""
    update_time = UpdateTimeDB(updated_date=rates_resp.date, updated_timestamp=rates_resp.timestamp)
    db_session.add(update_time)
    await db_session.commit()
    return update_time


async def get_time_update(db_session: AsyncSession) -> Optional[TimeDateResponse]:
    """Get date and unix timestamp for last currency update"""
    stmt = select(UpdateTimeDB).order_by(UpdateTimeDB.updated_timestamp.desc())
    res = await db_session.execute(stmt)
    resp = res.scalar()

    if resp:
        return TimeDateResponse(date=resp.updated_date, timestamp=resp.updated_timestamp)


async def get_db_currency_rates(db_session: AsyncSession, from_curr: str, to_curr: str = None) -> dict:
    """Get currency rate for one or two currencies"""
    from_curr_stmt = select(CurrencyDB).where(CurrencyDB.code == from_curr)
    to_curr_stmt = select(CurrencyDB).where(CurrencyDB.code == to_curr)

    db_res_from_curr = await db_session.execute(from_curr_stmt)
    db_res_to_curr = await db_session.execute(to_curr_stmt)

    to_curr_rate = db_res_to_curr.scalar()
    from_curr_rate = db_res_from_curr.scalar()
    if from_curr_rate and to_curr_rate:
        rates = dict(
            from_curr_rate=from_curr_rate.rate,
            to_curr_rate=to_curr_rate.rate,
            last_updated=from_curr_rate.updatetime.updated_timestamp,
        )
        return rates

    raise HTTPException(status_code=HTTPStatus.TOO_EARLY, detail={"detail": "No data in DB, please update rates"})
