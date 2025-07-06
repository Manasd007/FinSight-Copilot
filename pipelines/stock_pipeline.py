import yfinance as yf
import os
import pandas as pd

def fetch_stock_data(tickers, period="10y", interval="1d"):
    os.makedirs("data/stock_prices", exist_ok=True)
    for ticker in tickers:
        try:
            print(f"📈 Downloading stock data for {ticker}")
            df = yf.download(ticker, period=period, interval=interval, auto_adjust=False)

            if df.empty:
                print(f"⚠️ No data found for {ticker}")
                continue

            # Flatten MultiIndex if present
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(col).strip().lower() for col in df.columns.values]
            else:
                df.columns = df.columns.str.strip().str.lower()

            # Rename adj close to close if exists
            if 'adj close' in df.columns:
                df.rename(columns={'adj close': 'close'}, inplace=True)

            # Reset index so 'date' becomes a column
            df.reset_index(inplace=True)

            # Save to CSV
            file_path = f"data/stock_prices/{ticker}.csv"
            df.to_csv(file_path, index=False)
            print(f"✅ Saved stock data: {file_path}")

        except Exception as e:
            print(f"❌ Error fetching stock data for {ticker}: {e}")

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
    fetch_stock_data(tickers, period="5y")
