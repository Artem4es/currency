from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import String, Integer, Float, Column, DateTime, func, Date, BigInteger, ForeignKey


class CurrencyDB(Base):
    """
    - name: str (Russian Ruble, United States Dollar etc)
    - code: str (RUB, USD etc)
    - rate: float (Rate to 1 EUR)
updatetime_id@@1111111111111111111111111111111111111111111111111111111111111111111111145hgg54gf34332211111111!!
    """
    __tablename__ = "currency"
    code = Column(String, index=True, nullable=False, unique=True, primary_key=True)
    name = Column(String, index=True, nullable=False)
    rate = Column(Float, nullable=True, default=None)
    updatetime_id = Column(Integer, ForeignKey('updatetime.id'), nullable=True)
    updatetime = relationship('UpdateTimeDB', back_populates='currency', lazy="selectin")

class UpdateTimeDB(Base):
    __tablename__ = "updatetime"
    id = Column(Integer, primary_key=True)
    updated_date = Column(Date, nullable=True)
    updated_timestamp = Column(BigInteger, nullable=True)
    currency = relationship('CurrencyDB', back_populates='updatetime', lazy="selectin")



# Создайте отношение с помощью relationship
# CurrencyDB.updatetime = relationship('UpdateTimeDB', foreign_keys=[CurrencyDB.updatetime_id])