import os
import re
import pickle
from backend.finsight_app.path_utils import PROCESSED_DATA_DIR, EMBEDDINGS_DIR

PROCESSED_DIR = PROCESSED_DATA_DIR
MAPPING_PATH = os.path.join(EMBEDDINGS_DIR, 'chunk_mapping.pkl')

# Regex to extract ticker from any chunked file (10k, 10q, company_info, financial_data, stock_data, etc.)
CHUNK_RE = re.compile(r"([A-Za-z]+)_(?:10k|10q|company_info|financial_data|stock_data).*_chunk_\\d+\\.txt", re.IGNORECASE)

chunk_mapping = []

for fname in os.listdir(PROCESSED_DIR):
    match = CHUNK_RE.match(fname)
    if match:
        ticker = match.group(1).upper()
        chunk_mapping.append({
            "company": ticker,
            "file": fname
        })

with open(MAPPING_PATH, "wb") as f:
    pickle.dump(chunk_mapping, f)

print(f"Wrote {len(chunk_mapping)} entries to {MAPPING_PATH}") 