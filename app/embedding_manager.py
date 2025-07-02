# finsight_app/embedding_manager.py

from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingManager:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initializes the embedding model.
        """
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        """
        Encodes a list of texts into embedding vectors.
        Returns a NumPy array.
        """
        return self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    def encode_single(self, text):
        """
        Encodes a single string.
        """
        return self.encode([text])[0]
