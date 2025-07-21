import pytest
from fastapi.testclient import TestClient
from datetime import date
from main import app
from app.database import Base, engine, SessionLocal
from app.models import CurrencyRate


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[SessionLocal] = override_get_db
    return TestClient(app)


def test_successful_response(client, db):
    # Тестовые данные
    test_rate = CurrencyRate(
        date=date(2023, 3, 2),
        currency_code="USD",
        currency_name="Доллар США",
        nominal=1,
        value=75.50
    )
    db.add(test_rate)
    db.commit()

    response = client.get("/scripts/XML_daily.asp?date_req=02/03/2023")
    assert response.status_code == 200
    assert "ValCurs" in response.text
    assert "USD" in response.text


def test_error_response(client):
    for _ in range(5):
        response = client.get("/scripts/XML_daily.asp?date_req=01/01/2023")
        if response.status_code == 500:
            assert "Internal server error" in response.text
            return
    pytest.fail("No 500 response after 5 attempts")


def test_invalid_date_format(client):
    response = client.get("/scripts/XML_daily.asp?date_req=invalid-date")
    assert response.status_code == 400