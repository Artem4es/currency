from database import Base
from sqlalchemy import String, Integer, Float, Column, DateTime, func


class CurrencyDB(Base):
    """
    - name: str (Russian Ruble, United States Dollar etc)
    - code: str (RUB, USD etc)
    - rate: float (Rate to 1 EUR)
    - updated_at: auto field
    """
    __tablename__ = "currency"
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    rate = Column(Float, nullable=True, default=None)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())  ### время будет со сдвигом скорее всего!!!
