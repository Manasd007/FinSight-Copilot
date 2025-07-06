from backend.db.schema_postgres import SessionLocal, Company, Filing, StockPrice
import csv, os, pandas as pd
from datetime import datetime

# Use context manager for session lifecycle (SQLAlchemy 2.x best practice)
def insert_companies(session):
    with open("data/metadata/companies.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company = Company(
                ticker=row['Ticker'],
                name=row['Name'],
                sector=row['Sector'],
                industry=row['Industry'],
                market_cap=float(row['MarketCap']) if row['MarketCap'] else None,
                country=row['Country']
            )
            session.merge(company)
    session.commit()
    print("✅ Inserted companies into Postgres")

def insert_filings(session):
    filings_dir = "data/sec_filings"
    for ticker in os.listdir(filings_dir):
        ticker_dir = os.path.join(filings_dir, ticker)
        for file in os.listdir(ticker_dir):
            parts = file.replace(".html", "").split("_")
            form_type, date_str = parts[0], parts[1]
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            filing = Filing(
                ticker=ticker,
                form_type=form_type,
                date=date,
                filepath=os.path.join(ticker_dir, file)
            )
            session.add(filing)
    session.commit()
    print("✅ Inserted filings into Postgres")

def insert_stock_prices(session):
    prices_dir = "data/stock_prices"
    for file in os.listdir(prices_dir):
        ticker = file.replace(".csv", "")
        df = pd.read_csv(os.path.join(prices_dir, file))

        # Clean and normalize column names
        df.columns = df.columns.str.strip().str.lower()

        # Remove _ticker suffix (e.g., close_aapl → close)
        df.columns = [col.replace(f"_{ticker.lower()}", "") for col in df.columns]

        # Rename adj close → close if needed
        if 'adj close' in df.columns and 'close' not in df.columns:
            df.rename(columns={'adj close': 'close'}, inplace=True)

        # Required columns
        required_cols = ['date', 'open', 'high', 'low', 'close']
        if not all(col in df.columns for col in required_cols):
            print(f"⚠️ Skipping {ticker}: Missing required columns {set(required_cols) - set(df.columns)}")
            continue

        # Insert rows
        for _, row in df.iterrows():
            try:
                price = StockPrice(
                    ticker=ticker,
                    date=pd.to_datetime(row['date']).date(),
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    volume=row.get('volume', 0)
                )
                session.add(price)
            except Exception as e:
                print(f"❌ Error inserting stock price for {ticker}: {e}")

    session.commit()
    print("✅ Inserted stock prices into Postgres")

if __name__ == "__main__":
    with SessionLocal() as session:
        insert_companies(session)
        insert_filings(session)
        insert_stock_prices(session)