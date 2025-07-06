from fastapi import APIRouter, HTTPException
from backend.db.schema_postgres import SessionLocal, StockPrice

router = APIRouter()

@router.get("/{ticker}", summary="Get stock price history for a company")
def get_stock_prices(ticker: str):
    session = SessionLocal()
    try:
        prices = session.query(StockPrice).filter_by(ticker=ticker.upper()).order_by(StockPrice.date).all()
        if not prices:
            raise HTTPException(status_code=404, detail="No stock prices found for this company")
        return [
            {
                "date": p.date,
                "open": p.open,
                "high": p.high,
                "low": p.low,
                "close": p.close,
                "volume": p.volume
            }
            for p in prices
        ]
    finally:
        session.close() 