"""
FinSight Copilot - Complete RAG Pipeline
Combines retrieval and response generation for end-to-end question answering
"""

from finsight_app.retrieval_system import RetrievalSystem, retrieve_context
from finsight_app.llm_engine import generate_response
from typing import Dict, List, Optional
import os
from llama_cpp import Llama

# Path to your quantized .gguf model (update as needed)
MODEL_PATH = os.environ.get('LLAMA_MODEL_PATH', 'path/to/model.gguf')
llm = Llama(model_path=MODEL_PATH)

PROMPT_TEMPLATE = """
CONTEXT:
{context}

QUESTION: {question}

ANSWER:
"""

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
        print(f"🔍 Processing query: {query}")
        
        # Step 1: Retrieve relevant chunks
        print("📚 Retrieving relevant chunks...")
        retrieved_chunks = self.retriever.search(query, top_k=self.top_k)
        
        if not retrieved_chunks:
            return {
                "answer": "❌ No relevant information found in the documents.",
                "sources": [],
                "query": query,
                "chunks_retrieved": 0
            }
        
        print(f"✅ Retrieved {len(retrieved_chunks)} relevant chunks")
        
        # Step 2: Generate response
        print("🤖 Generating response...")
        answer = generate_response(query, retrieved_chunks, model_path)
        
        # Step 3: Prepare response with metadata
        response = {
            "answer": answer,
            "sources": retrieved_chunks,
            "query": query,
            "chunks_retrieved": len(retrieved_chunks),
            "pipeline": "RAG (Retrieval-Augmented Generation)"
        }
        
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
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 50)
        
        try:
            response = pipeline.answer_question(query)
            
            print(f"💬 Answer: {response['answer'][:300]}...")
            print(f"📊 Chunks retrieved: {response['chunks_retrieved']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ RAG Pipeline test completed!")

def answer_query(query, k=3, max_tokens=512):
    # Retrieve top-k context
    context_chunks = retrieve_context(query, k=k)
    context = '\n\n'.join(context_chunks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=query)
    print("Prompt sent to LLM:\n", prompt)
    output = llm(prompt, max_tokens=max_tokens)
    return output

if __name__ == "__main__":
    test_rag_pipeline() 