from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_app.crud import get_currency_rate


async def calculate_amount(db_session: AsyncSession, from_curr: str, to_curr: str, from_curr_amount: float) -> dict:
    """Calculate amount of 'to_curr' currency based on DB exchange rate"""
    curr_rates: dict = await get_currency_rate(db_session, from_curr, to_curr)

    from_curr_rate = curr_rates["from_curr_rate"]
    to_curr_rate = curr_rates["to_curr_rate"]
    last_updated = curr_rates["last_updated"]
    to_curr_amount: float = from_curr_amount * (to_curr_rate/from_curr_rate)
    curr_rates["result"] = to_curr_amount
    curr_rates["last_updated"] = last_updated
    return curr_rates   # может лучше можель Pydantic?
