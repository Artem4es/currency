from sqlalchemy import BigInteger, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class CurrencyDB(Base):
    """
    - code: str Primary Key (RUB, USD etc)
    - name: str (Russian Ruble, United States Dollar etc)
    - rate: float (Exchange rate to base currency (EUR by default))
    - updatetime_id int Foreign Key (Related to UpdateTimeDB. When currency was updated on ext. API)
    - updatetime: relationship to UpdateTimeDB.
    """

    __tablename__ = "currency"
    code = Column(String, index=True, nullable=False, unique=True, primary_key=True)
    name = Column(String, index=True, nullable=False)
    rate = Column(Float, nullable=True, default=None)
    updatetime_id = Column(Integer, ForeignKey("updatetime.id"), nullable=True)
    updatetime = relationship("UpdateTimeDB", back_populates="currency", lazy="selectin")


class UpdateTimeDB(Base):
    """
    - id: Primary Key
    - updated_date: str (When currency was updated on ext. API: '2002-11-10')
    - updated_timestamp: int (Unix timestamp when currency was updated on ext. API)
    - currency: relationship to CurrencyDB table.
    """

    __tablename__ = "updatetime"
    id = Column(Integer, primary_key=True, index=True)
    updated_date = Column(Date, nullable=True)
    updated_timestamp = Column(BigInteger, nullable=True)
    currency = relationship("CurrencyDB", back_populates="updatetime", lazy="selectin")
