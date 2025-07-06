from fastapi import FastAPI
from api.routes import companies, filings, stock_prices, graph

app = FastAPI(
    title="FinSight Copilot API",
    description="REST API for Postgres & Neo4j backend",
    version="1.0.0"
)

# Include Routers
app.include_router(companies.router, prefix="/companies")
app.include_router(filings.router, prefix="/filings")
app.include_router(stock_prices.router, prefix="/stock")
app.include_router(graph.router, prefix="/graph")

@app.get("/")
def root():
    return {"message": "Welcome to FinSight Copilot API 🚀"} 