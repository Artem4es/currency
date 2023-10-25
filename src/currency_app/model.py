from database import Base
from sqlalchemy import String, Integer, Float, Column, DateTime, func, Date, BigInteger


class CurrencyDB(Base):
    """
    - name: str (Russian Ruble, United States Dollar etc)
    - code: str (RUB, USD etc)
    - rate: float (Rate to 1 EUR)
    - updated_at: auto field
    updated_at Column(Date, nullable=True)         ### время будет со сдвигом скорее всего!!!
    unix_timestamp = Column(DateTime, nullable=True)
    """
    __tablename__ = "currency"
    code = Column(String, index=True, nullable=False, unique=True, primary_key=True)
    name = Column(String, index=True, nullable=False)
    rate = Column(Float, nullable=True, default=None)
    updated_date = Column(Date, nullable=True)         ### время будет со сдвигом скорее всего!!!  МОЖЕТ ЛИШНЕЕ!!
    updated_timestamp = Column(BigInteger, nullable=True)