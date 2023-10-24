from httpx import AsyncClient

from src.currency_app.schema import GetRates


async def get_currency_rates(client: AsyncClient) -> GetRates:
    """Get currency rates from external API"""
