from fastapi import APIRouter, HTTPException
from backend.db.schema_postgres import SessionLocal, Filing

router = APIRouter()

@router.get("/{ticker}", summary="Get filings for a company")
def get_filings(ticker: str):
    session = SessionLocal()
    try:
        filings = session.query(Filing).filter_by(ticker=ticker.upper()).all()
        if not filings:
            raise HTTPException(status_code=404, detail="No filings found for this company")
        return [
            {
                "id": f.id,
                "ticker": f.ticker,
                "form_type": f.form_type,
                "date": f.date,
                "filepath": f.filepath
            }
            for f in filings
        ]
    finally:
        session.close() 