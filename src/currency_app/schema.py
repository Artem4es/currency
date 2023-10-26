from enum import Enum
from typing import Optional

from pydantic import BaseModel, conint, constr, condate


# class Rates(BaseModel):
#     """Currency code and its rate"""
#     rates: dict[constr(pattern=r"^[A-Z]{3}$"), float]


class GetRates(BaseModel):
    """Response with rates from external API"""
    success: bool
    timestamp: conint(ge=0)
    base: constr(pattern=r"^[A-Z]{3}$")
    # date: constr(pattern=r'\d{4}-\d{2}-\d{2}')  # можно улучшить валидацию
    date: condate()  # можно улучшить валидацию
    rates: dict[constr(pattern=r"^[A-Z]{3}$"), float]
    # class Config:
    #     from_attributes=True


# class Symbols(BaseModel):
#     """Currency code and name"""
#     symbols: dict[constr(pattern=r"^[A-Z]{3}$"), str]


class GetCodes(BaseModel):
    """Get currency response names and codes"""
    success: bool
    symbols: dict[constr(pattern=r"^[A-Z]{3}$"), str]


class CurrencyUpdate(BaseModel):
    """Used for currency update in DB"""
    name: str
    code: str
    rate: Optional[float]
    # @validator("price")
    # @classmethod
    # def validate_price(cls, value):
    #     if value < 0:
    #         raise ValueError("Price must be non-negative")
    #     return value

class UpdateRespStatus(str, Enum):
    """Status for rates update"""
    SUCCESS = "Rates updated successfully"
    FAILED = "Couldn't update rates"


class UpdateRatesResponse(BaseModel):
    """Used for /update_rates" endpoint response"""
    status: UpdateRespStatus
    update_time: int


class TimeDateResponse(BaseModel):
    """Return date and unix timestamp for last currency update"""
    date: condate()
    timestamp: int


class ConvertResponse(BaseModel):
    """Response model for convert currency endpoint"""
    from_currency: str
    to_currency: str
    amount_from: float
    result: float
    last_updated: int
