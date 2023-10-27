from enum import Enum
import re
from pydantic import BaseModel, conint, constr, condate, validator, RootModel


class CurrencyCode(str):
    @classmethod
    def __get_validators__(cls, *args, **kwargs):
        yield cls.validate

    @classmethod
    def validate(cls, value, *args, **kwargs):
        if not re.match(r"^[A-Z]{3}$", value):
            raise ValueError("Invalid currency code. It should consist of 3 uppercase letters. example: USD")
        return value


class GetRates(BaseModel):
    """
    Get rates from external API

    - success: bool (Response status from ext. API)
    - timestamp: int (UNIX timestamp when rates were updated last time on ext. API)
    - base: CurrencyCode (Basic currency set in API Euro by default "EUR")
    - date condate (Date in '2030-12-25' format)
    - rates: dict (Currency rates example: {"USD": 1.2, "RUB": 150})
    """

    success: bool
    timestamp: conint(ge=0)
    base: CurrencyCode
    date: condate()
    rates: dict[CurrencyCode, float]


class GetCodes(BaseModel):
    """
    Get currency names and codes from ext. API

    - success: bool (Response status from ext. API)
    - codes: dict (Currency codes with full names: {"USD": "United Stated Dollar"})
    """
    success: bool
    codes: dict[CurrencyCode, str]


class UpdateRespStatus(str, Enum):
    """Status for rates update response"""
    SUCCESS = "Rates updated successfully"
    FAILED = "Couldn't update rates"


class UpdateRatesResponse(BaseModel):
    """Response data for /update_rates" endpoint"""
    status: UpdateRespStatus
    update_time: int


class TimeDateResponse(BaseModel):
    """Response data for '/last_update' endpoint.

    Both parameters mean last update in external API
    - date: condate (Date in '2030-12-25' format)
    - timestamp: int (UNIX timestamp)
    """
    date: condate()
    timestamp: int


class ConvertResponse(BaseModel):
    """
    Response model for '/convert' currency endpoint

    - from_currency: str (from what currency. Example "USD")
    - to_currency: str  (to what currency. Example "EUR")
    - amount: float  (amount to be converted)
    - result: float  (calculated amount of 'to_currency')
    - last_updated: conint  (currency last updated in ext. API unix timestamp)
    """
    from_currency: str
    to_currency: str
    amount: float
    result: float
    last_updated: conint(ge=0)


class CurrencyCodes:
    """
    All codes and description from DB. Fills in with data when app starts. Works as cache for DB codes

    Attribute example: USD = "United States Dollar"
    """
    pass

