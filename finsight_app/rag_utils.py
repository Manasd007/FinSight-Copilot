"""
FinSight Copilot - RAG Utilities
Core components for data processing, embeddings, and retrieval
"""

import json
import logging
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd
from tqdm import tqdm

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain.docstore.document import Document
from langchain.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Handles data cleaning, preprocessing, and chunking of financial documents
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the data processor
        
        Args:
            chunk_size: Size of text chunks in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess text data
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common financial document artifacts
        text = re.sub(r'Page \d+ of \d+', '', text)
        text = re.sub(r'Table of Contents', '', text)
        text = re.sub(r'Exhibit \d+', '', text)
        
        # Remove legal disclaimers (common in financial documents)
        disclaimer_patterns = [
            r'This document contains forward-looking statements.*?\.',
            r'Past performance does not guarantee future results.*?\.',
            r'This information is provided for informational purposes only.*?\.'
        ]
        
        for pattern in disclaimer_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove excessive punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
        
        # Remove multiple periods
        text = re.sub(r'\.{2,}', '.', text)
        
        return text.strip()
    
    def extract_financial_metrics(self, text: str) -> Dict[str, Any]:
        """
        Extract key financial metrics from text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of extracted metrics
        """
        metrics = {}
        
        # Revenue patterns
        revenue_patterns = [
            r'revenue.*?(\$[\d,]+\.?\d*[MBK]?)',
            r'total revenue.*?(\$[\d,]+\.?\d*[MBK]?)',
            r'net sales.*?(\$[\d,]+\.?\d*[MBK]?)'
        ]
        
        for pattern in revenue_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metrics['revenue'] = match.group(1)
                break
        
        # Profit patterns
        profit_patterns = [
            r'net income.*?(\$[\d,]+\.?\d*[MBK]?)',
            r'net profit.*?(\$[\d,]+\.?\d*[MBK]?)',
            r'operating income.*?(\$[\d,]+\.?\d*[MBK]?)'
        ]
        
        for pattern in profit_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metrics['profit'] = match.group(1)
                break
        
        # Growth patterns
        growth_patterns = [
            r'growth.*?(\d+\.?\d*%)',
            r'increase.*?(\d+\.?\d*%)',
            r'decrease.*?(\d+\.?\d*%)'
        ]
        
        for pattern in growth_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metrics['growth_rate'] = match.group(1)
                break
        
        return metrics
    
    def process_file(self, file_path: Path) -> List[Document]:
        """
        Process a single file and return chunks
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            List of Document objects
        """
        try:
            # Read file based on extension
            if file_path.suffix.lower() == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            elif file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
                text = df.to_string()
            elif file_path.suffix.lower() == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                text = json.dumps(data, indent=2)
            else:
                logger.warning(f"Unsupported file type: {file_path.suffix}")
                return []
            
            # Clean text
            cleaned_text = self.clean_text(text)
            
            # Extract metadata
            metadata = {
                'source': str(file_path),
                'file_type': file_path.suffix.lower(),
                'file_name': file_path.name,
                'metrics': self.extract_financial_metrics(cleaned_text)
            }
            
            # Split into chunks
            chunks = self.text_splitter.split_text(cleaned_text)
            
            # Create Document objects
            documents = []
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        **metadata,
                        'chunk_id': i,
                        'chunk_size': len(chunk)
                    }
                )
                documents.append(doc)
            
            logger.info(f"Processed {file_path.name}: {len(documents)} chunks created")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return []
    
    def save_chunks(self, chunks: List[Document], output_path: Path):
        """
        Save processed chunks to file
        
        Args:
            chunks: List of Document objects
            output_path: Path to save the chunks
        """
        try:
            # Convert to serializable format
            serializable_chunks = []
            for chunk in chunks:
                serializable_chunks.append({
                    'page_content': chunk.page_content,
                    'metadata': chunk.metadata
                })
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_chunks, f, indent=2)
            
            logger.info(f"Saved {len(chunks)} chunks to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving chunks: {e}")
            raise
    
    def load_chunks(self, input_path: Path) -> List[Document]:
        """
        Load processed chunks from file
        
        Args:
            input_path: Path to load chunks from
            
        Returns:
            List of Document objects
        """
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            chunks = []
            for item in data:
                doc = Document(
                    page_content=item['page_content'],
                    metadata=item['metadata']
                )
                chunks.append(doc)
            
            logger.info(f"Loaded {len(chunks)} chunks from {input_path}")
            return chunks
            
        except Exception as e:
            logger.error(f"Error loading chunks: {e}")
            return []

class EmbeddingManager:
    """
    Manages embedding generation and storage
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding manager
        
        Args:
            model_name: HuggingFace model name for embeddings
        """
        self.model_name = model_name
        self.embeddings = None
        self.vectorstore = None
        
    def create_embeddings(self, documents: List[Document], save_path: Optional[Path] = None):
        """
        Create embeddings for documents
        
        Args:
            documents: List of Document objects
            save_path: Optional path to save the vector store
        """
        try:
            logger.info(f"Creating embeddings for {len(documents)} documents using {self.model_name}")
            
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)
            
            # Create vector store
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            # Use FAISS for better performance
            self.vectorstore = FAISS.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas
            )
            
            # Save if path provided
            if save_path:
                self.vectorstore.save_local(str(save_path))
                logger.info(f"Vector store saved to {save_path}")
            
            logger.info("Embeddings created successfully")
            
        except Exception as e:
            logger.error(f"Error creating embeddings: {e}")
            raise
    
    def load_embeddings(self, load_path: Path):
        """
        Load existing embeddings
        
        Args:
            load_path: Path to load embeddings from
        """
        try:
            logger.info(f"Loading embeddings from {load_path}")
            
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)
            
            # Load vector store
            self.vectorstore = FAISS.load_local(str(load_path), self.embeddings)
            
            logger.info("Embeddings loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading embeddings: {e}")
            raise
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform similarity search
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Please create or load embeddings first.")
        
        return self.vectorstore.similarity_search(query, k=k)

class RetrievalSystem:
    """
    Advanced retrieval system with multiple retrieval strategies
    """
    
    def __init__(self, vectorstore: FAISS):
        """
        Initialize the retrieval system
        
        Args:
            vectorstore: FAISS vector store
        """
        self.vectorstore = vectorstore
        self.bm25_retriever = None
        self.ensemble_retriever = None
        
    def setup_bm25_retriever(self, documents: List[Document]):
        """
        Setup BM25 retriever for hybrid search
        
        Args:
            documents: List of Document objects
        """
        try:
            texts = [doc.page_content for doc in documents]
            self.bm25_retriever = BM25Retriever.from_texts(texts)
            logger.info("BM25 retriever initialized")
            
        except Exception as e:
            logger.error(f"Error setting up BM25 retriever: {e}")
    
    def setup_ensemble_retriever(self, weights: List[float] = None):
        """
        Setup ensemble retriever combining multiple strategies
        
        Args:
            weights: Weights for different retrievers
        """
        if not self.bm25_retriever:
            logger.warning("BM25 retriever not set up. Using vector store only.")
            return
        
        try:
            retrievers = [
                self.vectorstore.as_retriever(search_kwargs={"k": 5}),
                self.bm25_retriever
            ]
            
            if weights is None:
                weights = [0.7, 0.3]  # Give more weight to semantic search
            
            self.ensemble_retriever = EnsembleRetriever(
                retrievers=retrievers,
                weights=weights
            )
            
            logger.info("Ensemble retriever initialized")
            
        except Exception as e:
            logger.error(f"Error setting up ensemble retriever: {e}")
    
    def retrieve(self, query: str, k: int = 5, use_ensemble: bool = False) -> List[Document]:
        """
        Retrieve relevant documents
        
        Args:
            query: Search query
            k: Number of results to return
            use_ensemble: Whether to use ensemble retriever
            
        Returns:
            List of relevant documents
        """
        try:
            if use_ensemble and self.ensemble_retriever:
                return self.ensemble_retriever.get_relevant_documents(query)
            else:
                return self.vectorstore.similarity_search(query, k=k)
                
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return []
    
    def get_retrieval_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the retrieval system
        
        Returns:
            Dictionary with retrieval statistics
        """
        if not self.vectorstore:
            return {"error": "Vector store not initialized"}
        
        try:
            # Get basic stats
            stats = {
                "total_documents": self.vectorstore.index.ntotal,
                "embedding_dimension": self.vectorstore.index.d,
                "index_type": type(self.vectorstore.index).__name__,
                "has_bm25": self.bm25_retriever is not None,
                "has_ensemble": self.ensemble_retriever is not None
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting retrieval stats: {e}")
            return {"error": str(e)} 