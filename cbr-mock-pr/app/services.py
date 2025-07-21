from datetime import datetime
import random
from sqlalchemy.orm import Session
from .schemas import CurrencyRateCreate

CURRENCIES = [
    {"code": "USD", "name": "Доллар США"},
    {"code": "EUR", "name": "Евро"},
    {"code": "GBP", "name": "Фунт стерлингов"},
]


def generate_currency_data(db: Session, date_req: str):
    # Преобразование строки в объект date
    try:
        parsed_date = datetime.strptime(date_req, "%d/%m/%Y").date()
    except ValueError:
        parsed_date = datetime.strptime(date_req, "%Y-%m-%d").date()

    # Создание объекта с правильным форматом даты
    rates = []
    for currency in CURRENCIES:
        rate_data = CurrencyRateCreate(
            date=parsed_date,
            currency_code=currency["code"],
            currency_name=currency["name"],
            nominal=1,
            value=round(random.uniform(50, 100), 4)
        )
        rates.append(rate_data)

    return _format_xml_response(rates)


def _format_xml_response(rates):
    date_str = rates[0].date.strftime("%d.%m.%Y")
    xml = f'''<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="{date_str}" name="Foreign Currency Market">'''

    for rate in rates:
        xml += f'''
    <Valute ID="{rate.currency_code}">
        <NumCode>{random.randint(1, 999)}</NumCode>
        <CharCode>{rate.currency_code}</CharCode>
        <Nominal>{rate.nominal}</Nominal>
        <Name>{rate.currency_name}</Name>
        <Value>{rate.value:.4f}</Value>
    </Valute>'''

    return xml + "\n</ValCurs>"