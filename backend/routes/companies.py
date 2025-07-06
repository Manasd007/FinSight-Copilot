from fastapi import APIRouter
from finsight_app.rag_pipeline import query_company_data

router = APIRouter()

@router.get("/search")
def search_company(query: str):
    """
    Search for a company using RAG pipeline.
    """
    response = query_company_data(query)
    return {"result": response} 