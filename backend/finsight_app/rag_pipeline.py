"""
FinSight Copilot - Complete RAG Pipeline
Combines retrieval and response generation for end-to-end question answering
"""

from finsight_app.retrieval_system import RetrievalSystem, retrieve_context
from finsight_app.llm_engine import generate_response, gemini_response, GEMINI_API_KEY
from typing import Dict, List, Optional
import os
from llama_cpp import Llama
import numpy as np
import pickle
from sentence_transformers import util, SentenceTransformer
from finsight_app.path_utils import EMBEDDINGS_DIR, DATA_DIR

# Path to your quantized .gguf model (update as needed)
MODEL_PATH = os.environ.get('LLAMA_MODEL_PATH', 'path/to/model.gguf')

# Only load Llama if model exists
try:
    if os.path.exists(MODEL_PATH):
        llm = Llama(model_path=MODEL_PATH)
    else:
        llm = None
        print(f"⚠️ Llama model not found at {MODEL_PATH}. Using fallback responses.")
except Exception as e:
    llm = None
    print(f"⚠️ Error loading Llama model: {e}. Using fallback responses.")

PROMPT_TEMPLATE = """
CONTEXT:
{context}

QUESTION: {question}

ANSWER:
"""

DEBUG = os.getenv("DEBUG", "False") == "True"

EMBEDDINGS_PATH = os.path.join(EMBEDDINGS_DIR, "company_embeddings.npy")
MAPPING_PATH = os.path.join(EMBEDDINGS_DIR, "company_mapping.pkl")
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)
embeddings = np.load(EMBEDDINGS_PATH)
with open(MAPPING_PATH, "rb") as f:
    mapping = pickle.load(f)

class RAGPipeline:
    """
    Complete RAG pipeline for financial analysis
    """
    
    def __init__(self, top_k: int = 5):
        """
        Initialize the RAG pipeline
        
        Args:
            top_k: Number of top chunks to retrieve
        """
        self.retriever = RetrievalSystem()
        self.top_k = top_k
    
    def answer_question(self, query: str, model_path: Optional[str] = None) -> Dict[str, any]:
        """
        Answer a question using the complete RAG pipeline
        
        Args:
            query: User's question
            model_path: Path to local model (if using local LLM)
            
        Returns:
            Dictionary containing answer, sources, and metadata
        """
        if DEBUG:
            print(f"🔍 Processing query: {query}")
        
        # Step 1: Retrieve relevant chunks
        if DEBUG:
            print("📚 Retrieving relevant chunks...")
        retrieved_chunks = self.retriever.search(query, top_k=self.top_k)
        
        if not retrieved_chunks:
            # Fallback to Gemini if API key is set
            if GEMINI_API_KEY:
                if DEBUG:
                    print("⚠️ No chunks found, falling back to Gemini API...")
                prompt = f"Question: {query}\n\nPlease answer as best as you can."
                answer = gemini_response(prompt)
                return {
                    "answer": answer,
                    "sources": [],
                    "query": query,
                    "chunks_retrieved": 0,
                    "pipeline": "Gemini Fallback"
                }
            else:
                return {
                    "answer": "❌ No relevant information found in the documents.",
                    "sources": [],
                    "query": query,
                    "chunks_retrieved": 0
                }
        
        if DEBUG:
            print(f"✅ Retrieved {len(retrieved_chunks)} relevant chunks")
        
        # Step 2: Generate response
        if DEBUG:
            print("🤖 Generating response...")
        answer = generate_response(query, retrieved_chunks, model_path)
        # If local LLM fails or returns empty/error, fallback to Gemini
        if (not answer or answer.strip().startswith("❌")) and GEMINI_API_KEY:
            if DEBUG:
                print("⚠️ Local LLM failed or returned empty, falling back to Gemini API...")
            prompt = f"Question: {query}\n\nPlease answer as best as you can."
            answer = gemini_response(prompt)
            pipeline_used = "Gemini Fallback"
        else:
            pipeline_used = "RAG (Retrieval-Augmented Generation)"
        
        # Step 3: Prepare response with metadata
        response = {
            "answer": answer,
            "sources": retrieved_chunks,
            "query": query,
            "chunks_retrieved": len(retrieved_chunks),
            "pipeline": pipeline_used
        }
        
        if DEBUG:
            print("✅ Response generated successfully!")
        return response
    
    def analyze_financial_performance(self, company: str = "Apple") -> Dict[str, any]:
        """
        Analyze financial performance for a specific company
        
        Args:
            company: Company name to analyze
            
        Returns:
            Financial analysis response
        """
        query = f"Analyze {company}'s financial performance, revenue trends, and key business metrics"
        return self.answer_question(query)
    
    def get_risk_assessment(self, company: str = "Apple") -> Dict[str, any]:
        """
        Get risk assessment for a specific company
        
        Args:
            company: Company name to analyze
            
        Returns:
            Risk assessment response
        """
        query = f"What are the major risk factors affecting {company}'s business and financial performance?"
        return self.answer_question(query)
    
    def get_revenue_breakdown(self, company: str = "Apple") -> Dict[str, any]:
        """
        Get revenue breakdown for a specific company
        
        Args:
            company: Company name to analyze
            
        Returns:
            Revenue breakdown response
        """
        query = f"Break down {company}'s revenue by product and service categories"
        return self.answer_question(query)

    def answer(self, query, top_k=4, return_sources=False, model_path=None, company=None):
        """
        Answer a question with optional source return for UI.
        If company is specified, only retrieve chunks for that company.
        """
        if company:
            retrieved_chunks = self.retriever.search_by_company(query, company, top_k=top_k)
        else:
            retrieved_chunks = self.retriever.search(query, top_k=top_k)
        answer = generate_response(query, retrieved_chunks, model_path)
        if return_sources:
            return answer, retrieved_chunks
        return answer

def test_rag_pipeline():
    """Test the complete RAG pipeline"""
    if DEBUG:
        print("🚀 Testing FinSight Copilot RAG Pipeline")
        print("=" * 60)
    
    # Initialize pipeline
    pipeline = RAGPipeline(top_k=4)
    
    # Test queries
    test_queries = [
        "What were Apple's major revenue sources in 2023?",
        "What are the key risk factors affecting Apple's business?",
        "How did Apple's services business perform in 2023?",
        "What were Apple's financial highlights for 2023?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        if DEBUG:
            print(f"\n🔍 Test {i}: {query}")
            print("-" * 50)
        
        try:
            response = pipeline.answer_question(query)
            
            if DEBUG:
                print(f"💬 Answer: {response['answer'][:300]}...")
                print(f"📊 Chunks retrieved: {response['chunks_retrieved']}")
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Error: {e}")
    
    if DEBUG:
        print("\n" + "=" * 60)
        print("✅ RAG Pipeline test completed!")

def answer_query(query, k=3, max_tokens=512):
    # Retrieve top-k context
    context_chunks = retrieve_context(query, k=k)
    context = '\n\n'.join(context_chunks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=query)
    print("Prompt sent to LLM:\n", prompt)
    
    if llm is None:
        return "⚠️ Local LLM not available. Please set LLAMA_MODEL_PATH environment variable or use Gemini API."
    
    output = llm(prompt, max_tokens=max_tokens)
    return output

def query_company_data(query: str, top_k: int = 3):
    query_embedding = model.encode(query)
    scores = util.cos_sim(query_embedding, embeddings)[0]
    top_results = scores.argsort(descending=True)[:top_k]

    context = []
    for idx in top_results:
        context.append(f"Source: {mapping[idx]}\n---\n")
    return "\n".join(context)

if __name__ == "__main__":
    test_rag_pipeline() 