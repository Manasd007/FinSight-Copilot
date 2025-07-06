import os
import re
import pickle
from backend.finsight_app.path_utils import PROCESSED_DATA_DIR, EMBEDDINGS_DIR

PROCESSED_DIR = PROCESSED_DATA_DIR
MAPPING_PATH = os.path.join(EMBEDDINGS_DIR, 'chunk_mapping.pkl')

# Regex to extract ticker from filename (e.g., aapl_10k_2023_chunk_0.txt)
CHUNK_RE = re.compile(r"([a-zA-Z]+)_10k_\d{4}_chunk_\d+\.txt")

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