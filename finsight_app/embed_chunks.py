import os
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'processed_data')
EMBEDDINGS_PATH = os.path.join(os.path.dirname(__file__), '..', 'embeddings')

os.makedirs(EMBEDDINGS_PATH, exist_ok=True)

MODEL_NAME = 'all-MiniLM-L6-v2'

model = SentenceTransformer(MODEL_NAME)

chunk_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.txt') and '_chunk_' in f]
chunk_files.sort()

texts = []
file_mapping = []
for fname in chunk_files:
    with open(os.path.join(PROCESSED_DIR, fname), 'r', encoding='utf-8') as f:
        texts.append(f.read())
    file_mapping.append(fname)

print(f"Generating embeddings for {len(texts)} chunks...")
embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

# Save embeddings
embeddings_path = os.path.join(EMBEDDINGS_PATH, 'chunk_embeddings.npy')
np.save(embeddings_path, embeddings)

# Save mapping
mapping_path = os.path.join(EMBEDDINGS_PATH, 'chunk_mapping.pkl')
with open(mapping_path, 'wb') as f:
    pickle.dump(file_mapping, f)

print(f"Embeddings saved to {embeddings_path}")
print(f"Mapping saved to {mapping_path}") 