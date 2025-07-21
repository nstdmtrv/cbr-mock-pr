from datetime import date
from pydantic import BaseModel

class CurrencyRateCreate(BaseModel):
    date: date
    currency_code: str
    currency_name: str
    nominal: int
    value: float