from sqlalchemy.orm import Session
from . import models, schemas

def get_rates_by_date(db: Session, date: str):
    # Получение курсов валют по дате
    return db.query(models.CurrencyRate).filter(models.CurrencyRate.date == date).all()

def create_currency_rate(db: Session, rate: schemas.CurrencyRateCreate):
    # Создание новой записи о курсе валюты
    db_rate = models.CurrencyRate(**rate.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate