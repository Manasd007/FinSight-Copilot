import requests, os, time

HEADERS = {"User-Agent": "FinSightCopilot/1.0 (your-email@example.com)"}

def fetch_sec_filings(tickers, forms=["10-K", "10-Q"], years=5):
    for ticker in tickers:
        cik = get_cik(ticker)
        if not cik:
            print(f"⚠️ CIK not found for {ticker}")
            continue
        print(f"📥 Fetching filings for {ticker}")
        filings_url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
        try:
            r = requests.get(filings_url, headers=HEADERS)
            r.raise_for_status()
            filings = r.json().get("filings", {}).get("recent", {})
            save_filings(ticker, cik, filings, forms, years)
            time.sleep(0.5)  # Respect SEC rate limits
        except Exception as e:
            print(f"❌ Error fetching filings for {ticker}: {e}")

def get_cik(ticker):
    # Minimal example mapping
    mapping = {"AAPL": "0000320193", "MSFT": "0000789019", "GOOGL": "0001652044", "TSLA": "0001318605"}
    return mapping.get(ticker)

def save_filings(ticker, cik, filings, forms, years):
    os.makedirs(f"data/sec_filings/{ticker}", exist_ok=True)
    for form, date, accession in zip(filings["form"], filings["filingDate"], filings["accessionNumber"]):
        if form in forms and int(date[:4]) >= (2024 - years):
            doc_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession.replace('-', '')}/{accession}-index.html"
            filename = f"data/sec_filings/{ticker}/{form}_{date}.html"
            try:
                res = requests.get(doc_url, headers=HEADERS)
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(res.text)
                print(f"✅ Saved {form} for {ticker} ({date})")
            except Exception as e:
                print(f"❌ Error saving {form} for {ticker}: {e}")

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
    fetch_sec_filings(tickers, years=3) 