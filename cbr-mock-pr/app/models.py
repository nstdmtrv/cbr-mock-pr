from sqlalchemy import Column, Integer, String, Date, Float
from .database import Base

class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    currency_code = Column(String(3), index=True)
    currency_name = Column(String(50))
    nominal = Column(Integer)
    value = Column(Float)