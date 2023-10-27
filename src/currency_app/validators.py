from fastapi import Query, HTTPException
from http import HTTPStatus

from src.currency_app.schema import CurrencyCodes


def validate_from_curr(from_curr: str = Query(description="Currency code in uppercase (e.g., USD)", regex=r"^[A-Z]{3}$")) -> str:
    """Validate currency code (exists or not in DB)"""
    if not hasattr(CurrencyCodes, from_curr):
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"Invalid currency code: '{from_curr}'. It doesn't exist in database")

    return from_curr


def validate_to_curr(to_curr: str = Query(description="Currency code in uppercase (e.g., USD)", regex=r"^[A-Z]{3}$")) -> str:
    """Validate currency code (exists or not in DB)"""
    if not hasattr(CurrencyCodes, to_curr):
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"Invalid currency code: '{to_curr}'. It doesn't exist in database")

    return to_curr


def validate_curr_amount(from_curr_amount: float = Query(description="Any positive number. Point separated: 1.556)")) -> float:
    """Validate amount to be changed"""
    if from_curr_amount < 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Amount can't be lower than 0!")

    return from_curr_amount
