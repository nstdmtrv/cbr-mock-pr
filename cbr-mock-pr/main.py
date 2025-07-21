from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse
from datetime import datetime
from app.database import SessionLocal, engine
from app import models
from app.services import generate_currency_data
import random

# Инициализация БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CBR Mock Service",
    description="Mock service for Central Bank of Russia currency rates API",
    version="1.0.0",
)

@app.get("/scripts/XML_daily.asp", response_class=PlainTextResponse)
async def get_currency_rates(date_req: str):
    try:
        datetime.strptime(date_req, "%d/%m/%Y").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use DD/MM/YYYY",
        )

    if random.random() < 0.5:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    db = SessionLocal()
    try:
        currency_data = generate_currency_data(db, date_req)
        return currency_data
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)