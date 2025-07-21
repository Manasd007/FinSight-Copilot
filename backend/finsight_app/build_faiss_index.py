import os
import numpy as np
import faiss
from backend.finsight_app.path_utils import get_faiss_index_dir, EMBEDDINGS_DIR

EMBEDDINGS_PATH = get_faiss_index_dir()

embeddings_file = os.path.join(EMBEDDINGS_DIR, 'company_embeddings.npy')
faiss_index_dir = EMBEDDINGS_PATH
faiss_index_file = os.path.join(faiss_index_dir, 'index.faiss')

# Load embeddings
embeddings = np.load(embeddings_file)
embedding_dim = embeddings.shape[1]
print(f"Loaded embeddings: {embeddings.shape}")

# Build FAISS index
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)
print(f"FAISS index built. Total vectors: {index.ntotal}")

# Ensure output directory exists
os.makedirs(faiss_index_dir, exist_ok=True)

# Save index
faiss.write_index(index, faiss_index_file)
print(f"FAISS index saved to {faiss_index_file}") 