from fastapi import APIRouter, HTTPException, Query
from backend.db.schema_postgres import SessionLocal, Company
from backend.finsight_app.rag_pipeline import query_company_data

router = APIRouter()

@router.get("/", summary="List all companies")
def list_companies():
    session = SessionLocal()
    try:
        companies = session.query(Company).all()
        return [
            {
                "ticker": c.ticker,
                "name": c.name,
                "sector": c.sector,
                "industry": c.industry,
                "market_cap": c.market_cap,
                "country": c.country
            }
            for c in companies
        ]
    finally:
        session.close()

@router.get("/{ticker}", summary="Get metadata for a company")
def get_company(ticker: str):
    session = SessionLocal()
    try:
        company = session.query(Company).filter_by(ticker=ticker.upper()).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return {
            "ticker": company.ticker,
            "name": company.name,
            "sector": company.sector,
            "industry": company.industry,
            "market_cap": company.market_cap,
            "country": company.country
        }
    finally:
        session.close()

@router.get("/search")
def search_company(query: str = Query(..., description="Company name or ticker")):
    """
    Search company using RAG pipeline
    """
    result = query_company_data(query)
    return {"result": result} 