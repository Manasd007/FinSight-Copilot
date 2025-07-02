import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os
import numpy as np

class RetrievalSystem:
    def __init__(self, index_dir="embeddings", processed_dir="processed_data", model_name="all-MiniLM-L6-v2"):
        self.index_dir = index_dir
        self.processed_dir = processed_dir
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(os.path.join(index_dir, "finsight_index.faiss"))
        with open(os.path.join(index_dir, "chunk_mapping.pkl"), "rb") as f:
            self.chunk_files = pickle.load(f)

    def search(self, query, top_k=5):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        results = []

        for idx in indices[0]:
            meta = self.chunk_files[idx]
            file_path = os.path.join(self.processed_dir, meta["file"])
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            results.append(content)

        return results

    def search_by_company(self, query, company, top_k=5):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k * 2)  # get more and filter
        results = []
        count = 0
        for idx in indices[0]:
            meta = self.chunk_files[idx]
            if meta["company"] == company:
                file_path = os.path.join(self.processed_dir, meta["file"])
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                results.append(content)
                count += 1
                if count >= top_k:
                    break
        return results

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'processed_data')
EMBEDDINGS_PATH = os.path.join(os.path.dirname(__file__), '..', 'embeddings')
MODEL_NAME = 'all-MiniLM-L6-v2'

# Load model, index, and mapping once
model = SentenceTransformer(MODEL_NAME)
faiss_index_file = os.path.join(EMBEDDINGS_PATH, 'finsight_index.faiss')
chunk_mapping_file = os.path.join(EMBEDDINGS_PATH, 'chunk_mapping.pkl')

index = faiss.read_index(faiss_index_file)
with open(chunk_mapping_file, 'rb') as f:
    chunk_mapping = pickle.load(f)

# Preload chunk texts
chunk_texts = {}
for fname in chunk_mapping:
    path = os.path.join(PROCESSED_DIR, fname)
    with open(path, 'r', encoding='utf-8') as f:
        chunk_texts[fname] = f.read()

def retrieve_context(query, k=3):
    query_emb = model.encode([query])
    D, I = index.search(query_emb, k)
    results = []
    for idx in I[0]:
        fname = chunk_mapping[idx]
        print(f"Retrieved chunk idx: {idx}, file: {fname}")
        results.append(chunk_texts[fname])
    return results 