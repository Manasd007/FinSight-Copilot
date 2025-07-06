from py2neo import Graph, Node, Relationship
import csv, os

# Connect to Neo4j
graph = Graph("neo4j://127.0.0.1:7687", auth=("neo4j", "Password"))

def create_company_nodes(metadata_path="data/metadata/companies.csv"):
    with open(metadata_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company = Node(
                "Company",
                ticker=row["Ticker"],
                name=row["Name"],
                sector=row["Sector"],
                industry=row["Industry"],
                market_cap=row["MarketCap"],
                country=row["Country"]
            )
            graph.merge(company, "Company", "ticker")
            print(f"✅ Added Company node: {row['Ticker']}")

def create_filing_nodes():
    filings_dir = "data/sec_filings"
    for ticker in os.listdir(filings_dir):
        company = graph.nodes.match("Company", ticker=ticker).first()
        if not company:
            print(f"⚠️ Company node missing for {ticker}")
            continue
        ticker_dir = os.path.join(filings_dir, ticker)
        for file in os.listdir(ticker_dir):
            if file.endswith(".html"):
                parts = file.replace(".html", "").split("_")
                form_type, date = parts[0], parts[1]
                filing = Node("Filing", form_type=form_type, date=date, path=os.path.join(ticker_dir, file))
                graph.merge(filing, "Filing", "path")
                rel = Relationship(company, "FILED", filing)
                graph.merge(rel)
                print(f"📄 Linked {form_type} filing ({date}) to {ticker}")

def create_sector_relationships():
    for company in graph.nodes.match("Company"):
        sector_name = company["sector"]
        if sector_name:
            sector = Node("Sector", name=sector_name)
            graph.merge(sector, "Sector", "name")
            rel = Relationship(company, "BELONGS_TO", sector)
            graph.merge(rel)
            print(f"🔗 Linked {company['ticker']} to sector {sector_name}")

if __name__ == "__main__":
    create_company_nodes()
    create_filing_nodes()
    create_sector_relationships() 