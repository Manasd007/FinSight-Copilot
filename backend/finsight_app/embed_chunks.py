import os
import json
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from backend.finsight_app.path_utils import DATA_DIR, EMBEDDINGS_DIR

# Paths
PROCESSED_DIR = DATA_DIR  # Use DATA_DIR for processed data
EMBEDDINGS_PATH = os.path.join(EMBEDDINGS_DIR, "chunk_embeddings.npy")

os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

MODEL_NAME = 'all-MiniLM-L6-v2'
model = SentenceTransformer(MODEL_NAME)

# Find JSON files
json_files = [f for f in os.listdir(DATA_DIR) if f.endswith('_company_info.json') or f.endswith('_financial_data.json')]
print("JSON files found:", json_files)
json_files.sort()

texts = []
file_mapping = []

# Load JSON and extract text
for fname in json_files:
    path = os.path.join(DATA_DIR, fname)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Combine fields for embedding
        content = json.dumps(data, indent=2)
        texts.append(content)
        file_mapping.append(fname)

print(f"Generating embeddings for {len(texts)} company JSON files...")
embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

# Save embeddings
embeddings_path = os.path.join(EMBEDDINGS_DIR, 'company_embeddings.npy')
np.save(embeddings_path, embeddings)

# Save mapping
mapping_path = os.path.join(EMBEDDINGS_DIR, 'company_mapping.pkl')
with open(mapping_path, 'wb') as f:
    pickle.dump(file_mapping, f)

print(f"✅ Embeddings saved to {embeddings_path}")
print(f"✅ Mapping saved to {mapping_path}")
