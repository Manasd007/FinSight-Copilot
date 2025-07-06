from sqlalchemy import create_engine, Column, String, Float, Date, Integer, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import csv, os, pandas as pd

# PostgreSQL connection string
DATABASE_URL = "postgresql://postgres:Password@localhost:5432/finsight"

# Setup
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Models
class Company(Base):
    __tablename__ = 'companies'
    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)
    industry = Column(String)
    market_cap = Column(Float)
    country = Column(String)
    filings = relationship("Filing", back_populates="company")
    prices = relationship("StockPrice", back_populates="company")

class Filing(Base):
    __tablename__ = 'filings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, ForeignKey('companies.ticker'))
    form_type = Column(String)
    date = Column(Date)
    filepath = Column(String)
    company = relationship("Company", back_populates="filings")

class StockPrice(Base):
    __tablename__ = 'stock_prices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, ForeignKey('companies.ticker'))
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    company = relationship("Company", back_populates="prices")

# Create tables
Base.metadata.create_all(bind=engine)

# Test the connection
if __name__ == "__main__":
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print(result.fetchone()) 