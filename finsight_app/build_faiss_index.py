import os
import numpy as np
import faiss

EMBEDDINGS_PATH = os.path.join(os.path.dirname(__file__), '..', 'embeddings')

embeddings_file = os.path.join(EMBEDDINGS_PATH, 'chunk_embeddings.npy')
faiss_index_file = os.path.join(EMBEDDINGS_PATH, 'finsight_index.faiss')

# Load embeddings
embeddings = np.load(embeddings_file)
embedding_dim = embeddings.shape[1]
print(f"Loaded embeddings: {embeddings.shape}")

# Build FAISS index
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)
print(f"FAISS index built. Total vectors: {index.ntotal}")

# Save index
faiss.write_index(index, faiss_index_file)
print(f"FAISS index saved to {faiss_index_file}") 