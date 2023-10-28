from time import time

from config import Settings
from src.currency_app.schemas import GetRates

settings = Settings()


class UpdateManager:
    """Used basically for caching currency data"""

    def __init__(self, expiration_period: int, currency_data: GetRates = None):
        self.currency_data = currency_data
        self.expiration_period = expiration_period

    def has_expired(self) -> bool:
        """Cached currency data has expired or not"""
        current_time = time()
        return (current_time - self.currency_data.timestamp) > self.expiration_period

    def expires_in(self) -> int:
        """Time until expiration"""
        current_time = time()
        return int(self.expiration_period - (current_time - self.currency_data.timestamp))

    def last_updated(self) -> int:
        """Currency was last updated on ext. API (Cached result could be expired)"""
        return self.currency_data.timestamp

    def get_currency_data(self) -> GetRates:
        """Return lastly fetched currency data"""
        return self.currency_data

    def get_currency_rate(self, curr_code) -> float:
        """Return cached currency rate for given code"""
        rates: dict = self.currency_data.rates
        return rates[curr_code]

    def update_currency_data(self, currency_data: GetRates) -> None:
        """Refresh cached currency data"""
        self.currency_data = currency_data


update_manager = UpdateManager(expiration_period=settings.expiration_period)
