import os
from typing import List, Optional

# Configuration - Set to True to use Gemini API, False for local LLM
USE_GEMINI = False

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def build_prompt(query: str, retrieved_chunks: List[str]) -> str:
    """
    Build a prompt for the LLM using the query and retrieved chunks
    
    Args:
        query: User's question
        retrieved_chunks: List of relevant text chunks
        
    Returns:
        Formatted prompt for the LLM
    """
    context = "\n\n".join(retrieved_chunks)
    prompt = f"""You are FinSight Copilot, a financial analysis assistant. You help users understand financial documents and provide insights based on the provided context.

Context from financial documents:
{context}

Question: {query}

Please provide a clear, accurate, and informative answer based on the context above. If the context doesn't contain enough information to answer the question, please say so. Focus on financial insights and business analysis.

Answer:"""
    return prompt

def gemini_response(prompt: str) -> str:
    """
    Generate response using Gemini API
    
    Args:
        prompt: Formatted prompt for the LLM
        
    Returns:
        Generated response text
    """
    try:
        import google.generativeai as genai
        
        if not GEMINI_API_KEY:
            return "❌ Error: Gemini API key not configured. Please set GEMINI_API_KEY environment variable."
        
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
        
    except ImportError:
        return "❌ Error: google-generativeai package not installed. Run: pip install google-generativeai"
    except Exception as e:
        return f"❌ Error generating Gemini response: {str(e)}"

def local_llm_response(prompt: str, model_path: str = "models/phi-2.gguf") -> str:
    """
    Generate response using local LLM (llama-cpp-python)
    
    Args:
        prompt: Formatted prompt for the LLM
        model_path: Path to the GGUF model file
        
    Returns:
        Generated response text
    """
    try:
        from llama_cpp import Llama
        
        if not os.path.exists(model_path):
            return f"❌ Error: Local model not found at {model_path}. Please download a GGUF model first."
        
        llm = Llama(model_path=model_path, n_ctx=2048, verbose=False)
        
        output = llm(
            prompt=prompt, 
            max_tokens=500, 
            temperature=0.7,
            stop=["User:", "AI:", "\n\nQuestion:", "Context:"]
        )
        
        return output["choices"][0]["text"].strip()
        
    except ImportError:
        return "❌ Error: llama-cpp-python package not installed. Run: pip install llama-cpp-python"
    except Exception as e:
        return f"❌ Error generating local LLM response: {str(e)}"

def generate_response(query: str, retrieved_chunks: List[str], model_path: Optional[str] = None) -> str:
    """
    Main function to generate a response using the configured LLM
    
    Args:
        query: User's question
        retrieved_chunks: List of relevant text chunks
        model_path: Path to local model (if using local LLM)
        
    Returns:
        Generated response text
    """
    # Build the prompt
    prompt = build_prompt(query, retrieved_chunks)
    
    # Generate response based on configuration
    if USE_GEMINI:
        print("🤖 Using Gemini API for response generation...")
        return gemini_response(prompt)
    else:
        print("🏠 Using local LLM for response generation...")
        if model_path is None:
            model_path = "models/phi-2.gguf"
        return local_llm_response(prompt, model_path)

# Convenience function for testing
def test_llm_engine():
    """Test the LLM engine with a sample query and chunks"""
    test_query = "What were Apple's major revenue sources in 2023?"
    test_chunks = [
        "iPhone net sales were $200,583 million in 2023, representing the largest revenue source.",
        "Services net sales were $85,200 million in 2023, showing strong growth in recurring revenue.",
        "Mac net sales were $29,357 million in 2023, down from previous year due to market conditions."
    ]
    
    print("🧪 Testing LLM Engine...")
    print(f"Query: {test_query}")
    print(f"Configuration: {'Gemini API' if USE_GEMINI else 'Local LLM'}")
    print("-" * 50)
    
    response = generate_response(test_query, test_chunks)
    print(f"Response: {response}")

if __name__ == "__main__":
    test_llm_engine() 