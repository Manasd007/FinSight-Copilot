import os
import re
import pickle

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'processed_data')
MAPPING_PATH = os.path.join(os.path.dirname(__file__), '..', 'embeddings', 'chunk_mapping.pkl')

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