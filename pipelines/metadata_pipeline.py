import yfinance as yf
import csv
import os

def fetch_metadata(tickers):
    os.makedirs("data/metadata", exist_ok=True)
    metadata = []
    for ticker in tickers:
        try:
            print(f"Fetching metadata for {ticker}")
            info = yf.Ticker(ticker).info
            metadata.append({
                "Ticker": ticker,
                "Name": info.get("shortName"),
                "Sector": info.get("sector"),
                "Industry": info.get("industry"),
                "MarketCap": info.get("marketCap"),
                "Country": info.get("country")
            })
        except Exception as e:
            print(f"Error fetching metadata for {ticker}: {e}")

    # Save to CSV
    filepath = "data/metadata/companies.csv"
    if metadata:
        keys = metadata[0].keys()
        with open(filepath, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(metadata)
        print(f"Metadata saved to {filepath}")
    else:
        print("No metadata fetched.")

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
    fetch_metadata(tickers) 