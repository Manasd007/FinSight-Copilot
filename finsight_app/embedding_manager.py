import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

class EmbeddingManager:
    def __init__(self, data_dir="processed_data", index_dir="embeddings", model_name="all-MiniLM-L6-v2"):
        self.data_dir = data_dir
        self.index_dir = index_dir
        os.makedirs(index_dir, exist_ok=True)
        self.model = SentenceTransformer(model_name)

    def load_chunks(self):
        chunks = []
        file_names = []

        for file in os.listdir(self.data_dir):
            if file.endswith(".txt") and "_chunk_" in file:
                path = os.path.join(self.data_dir, file)
                with open(path, "r", encoding="utf-8") as f:
                    chunks.append(f.read())
                    file_names.append(file)

        return chunks, file_names

    def create_and_save_faiss_index(self):
        chunks, file_names = self.load_chunks()
        print(f"📦 Loaded {len(chunks)} chunks... Generating embeddings...")

        embeddings = self.model.encode(chunks, show_progress_bar=True)

        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        faiss.write_index(index, os.path.join(self.index_dir, "finsight_index.faiss"))

        with open(os.path.join(self.index_dir, "chunk_mapping.pkl"), "wb") as f:
            pickle.dump(file_names, f)

        print("✅ FAISS index and metadata saved!")

    def load_index(self):
        index = faiss.read_index(os.path.join(self.index_dir, "finsight_index.faiss"))
        with open(os.path.join(self.index_dir, "chunk_mapping.pkl"), "rb") as f:
            file_names = pickle.load(f)
        return index, file_names 