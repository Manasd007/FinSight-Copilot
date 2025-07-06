import os

# Project base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Unified data directories
DATA_DIR = os.path.join(BASE_DIR, "backend", "data")
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "backend", "embeddings")
LOGS_DIR = os.path.join(BASE_DIR, "backend", "logs")
MODELS_DIR = os.path.join(BASE_DIR, "backend", "models")
DB_DIR = os.path.join(BASE_DIR, "db")

# Subfolders
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed_data")
SEC_FILINGS_DIR = os.path.join(DATA_DIR, "sec_filings")
STOCK_PRICES_DIR = os.path.join(DATA_DIR, "stock_prices")
 
def get_faiss_index_dir() -> str:
    """Returns the absolute path to the FAISS index directory."""
    return os.path.join(EMBEDDINGS_DIR, "finsight_index")

def ensure_directories():
    """Ensure all necessary directories exist."""
    directories = [
        DATA_DIR,
        EMBEDDINGS_DIR,
        LOGS_DIR,
        MODELS_DIR,
        PROCESSED_DATA_DIR,
        SEC_FILINGS_DIR,
        STOCK_PRICES_DIR,
        get_faiss_index_dir()
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    return directories 