import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os
import numpy as np
from backend.finsight_app.path_utils import (
    get_faiss_index_dir, 
    DATA_DIR, 
    EMBEDDINGS_DIR, 
    PROCESSED_DATA_DIR
)

class RetrievalSystem:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.index_dir = get_faiss_index_dir()
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(os.path.join(self.index_dir, "index.faiss"))
        with open(os.path.join(self.index_dir, "chunk_mapping.pkl"), "rb") as f:
            self.chunk_files = pickle.load(f)

    def search(self, query, top_k=5):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        results = []

        for idx in indices[0]:
            meta = self.chunk_files[idx]
            file_path = os.path.join(PROCESSED_DATA_DIR, meta["file"])
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
                file_path = os.path.join(PROCESSED_DATA_DIR, meta["file"])
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                results.append(content)
                count += 1
                if count >= top_k:
                    break
        return results

# Global constants using new path structure
EMBEDDINGS_PATH = get_faiss_index_dir()
MODEL_NAME = 'all-MiniLM-L6-v2'

# Load model, index, and mapping once - with error handling
model = SentenceTransformer(MODEL_NAME)

# Try to load company mapping and index, but don't fail if files don't exist
try:
    company_mapping_file = os.path.join(EMBEDDINGS_DIR, "company_mapping.pkl")
    if os.path.exists(company_mapping_file):
        with open(company_mapping_file, 'rb') as f:
            mapping = pickle.load(f)
    else:
        print(f"⚠️ Company mapping file not found: {company_mapping_file}")
        mapping = []
except Exception as e:
    print(f"⚠️ Error loading company mapping: {e}")
    mapping = []

try:
    faiss_index_file = os.path.join(EMBEDDINGS_DIR, "finsight_index", "index.faiss")
    if os.path.exists(faiss_index_file):
        index = faiss.read_index(faiss_index_file)
    else:
        print(f"⚠️ FAISS index file not found: {faiss_index_file}")
        index = None
except Exception as e:
    print(f"⚠️ Error loading FAISS index: {e}")
    index = None

# Preload chunk texts - with error handling
chunk_texts = {}
if mapping and os.path.exists(PROCESSED_DATA_DIR):
    for fname in mapping:
        path = os.path.join(PROCESSED_DATA_DIR, fname)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    chunk_texts[fname] = f.read()
            except Exception as e:
                print(f"⚠️ Error loading chunk {fname}: {e}")
        else:
            print(f"⚠️ Chunk file not found: {path}")

def retrieve_context(query, k=3):
    if not index or not mapping:
        print("⚠️ Index or mapping not available")
        return []
    
    query_emb = model.encode([query])
    D, I = index.search(query_emb, k)
    results = []
    for idx in I[0]:
        if idx < len(mapping):
            fname = mapping[idx]
            print(f"Retrieved chunk idx: {idx}, file: {fname}")
            if fname in chunk_texts:
                results.append(chunk_texts[fname])
    return results

CHUNK_MAPPING_FILE = os.path.join(EMBEDDINGS_DIR, "chunk_mapping.pkl") 