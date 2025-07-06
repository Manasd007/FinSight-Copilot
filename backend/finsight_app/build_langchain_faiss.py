from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import os
import pickle
from backend.finsight_app.path_utils import get_faiss_index_dir, PROCESSED_DATA_DIR, EMBEDDINGS_DIR

EMBEDDINGS_DIR_PATH = get_faiss_index_dir()
PROCESSED_DIR = PROCESSED_DATA_DIR
INDEX_PATH = EMBEDDINGS_DIR_PATH
CHUNK_MAPPING_PATH = os.path.join(EMBEDDINGS_DIR, 'chunk_mapping.pkl')

# Load chunk mapping
with open(CHUNK_MAPPING_PATH, 'rb') as f:
    chunk_mapping = pickle.load(f)

# Build Document objects from chunk files
documents = []
for meta in chunk_mapping:
    fname = meta['file'] if isinstance(meta, dict) and 'file' in meta else meta
    chunk_path = os.path.join(PROCESSED_DIR, fname)
    with open(chunk_path, 'r', encoding='utf-8') as f:
        text = f.read()
    documents.append(Document(page_content=text, metadata={'file': fname}))

print(f"Loaded {len(documents)} documents. Building FAISS index...")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(documents, embedding_model)
vectorstore.save_local(INDEX_PATH)

print(f"✅ FAISS index and mapping saved to {INDEX_PATH}") 