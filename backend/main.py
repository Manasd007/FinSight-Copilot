import os
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env and .env.local
load_dotenv()  # Load .env
load_dotenv('.env.local')  # Load .env.local

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_cpp import Llama
from sentence_transformers import CrossEncoder
import google.generativeai as genai

from finsight_app.prompts import FinSightPrompts, PromptType, PromptConfig
from finsight_app.rag_utils import RetrievalSystem
from finsight_app.upload import router as upload_router
from finsight_app.path_utils import get_faiss_index_dir
from routes.chat_history import router as chat_history_router
from routes.trading import router as trading_router


# ==== FastAPI Init ====
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== Load Embedding Model ====
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ==== Load FAISS Vectorstore Safely ====
faiss_index_path = get_faiss_index_dir()
index_file_path = os.path.join(faiss_index_path, "index.faiss")
assert os.path.exists(index_file_path), f"❌ FAISS index file missing at {index_file_path}"
print(f"✅ FAISS index found at: {index_file_path}")

vectorstore = FAISS.load_local(faiss_index_path, embeddings=embedding_model, allow_dangerous_deserialization=True)
retriever = RetrievalSystem(vectorstore=vectorstore)

# ==== Load Local Hugging Face LLM Engine ====
from finsight_app.local_hf_engine import LocalHuggingFaceEngine

# ✅ Initialize Local Hugging Face LLM Engine
try:
    llm = LocalHuggingFaceEngine("microsoft/DialoGPT-medium")
    print("✅ Local Hugging Face LLM Engine initialized")
    
    # Test connection
    if llm.test_connection():
        print("✅ Local Hugging Face model loaded successfully")
    else:
        print("⚠️ Local Hugging Face model failed to load, will use Gemini fallback")
        
except Exception as e:
    print(f"⚠️ Failed to initialize Local Hugging Face LLM: {e}")
    print("🔄 Will use Gemini fallback for all requests")
    llm = None

# ==== Prompt System ====
prompt_builder = FinSightPrompts()

# ==== Load Reranker (Faster Model) ====
reranker = CrossEncoder("cross-encoder/qnli-distilroberta-base")

# ==== Gemini API Fallback ====
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"✅ Gemini API key configured: {GEMINI_API_KEY[:10]}...")
else:
    print("⚠️ No Gemini API key found in environment variables")

def gemini_fallback(question: str):
    try:
        if not GEMINI_API_KEY:
            return "❌ Gemini API key not configured. Please set GEMINI_API_KEY environment variable."
        
        print(f"🔮 Calling Gemini API with question: {question[:50]}...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        res = model.generate_content(question)
        
        if res and res.text:
            answer = res.text.strip()
            print(f"✅ Gemini response: {answer[:100]}...")
            return answer
        else:
            print("❌ Gemini returned empty response")
            return "❌ Sorry, I couldn't generate a response. Please try again."
            
    except Exception as e:
        print(f"❌ Gemini API error: {str(e)}")
        return f"❌ Gemini API error: {str(e)}"


# ==== Rerank Function ====
def rerank(question, chunks, top_k=3):
    pairs = [[question, chunk.page_content if hasattr(chunk, 'page_content') else str(chunk)] for chunk in chunks]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
    print("\n🔎 RERANKED CHUNKS (top 3):")
    for i, (chunk, score) in enumerate(ranked[:top_k]):
        print(f"[{i+1}] Score: {score:.4f} | {chunk.page_content[:200]}...\n")
    return [chunk for chunk, score in ranked[:top_k]]


# ==== Request Schema ====
class AskRequest(BaseModel):
    question: str

class ChatRequest(BaseModel):
    query: str


# ==== POST /ask ====
@app.post("/ask")
async def ask(request: AskRequest):
    try:
        question = request.question
        print(f"\n📥 QUESTION: {question}")
        
        context_chunks = retriever.retrieve(question, k=3)
        reranked_chunks = rerank(question, context_chunks, top_k=3)
        # Step 2: Limit context size and deduplicate sentences
        from collections import OrderedDict
        def dedup_and_truncate(chunks, max_chars=800):
            seen = OrderedDict()
            total = 0
            for chunk in chunks:
                for sentence in chunk.page_content.split('. '):
                    sentence = sentence.strip()
                    if sentence and sentence not in seen:
                        if total + len(sentence) + 2 > max_chars:
                            break
                        seen[sentence] = True
                        total += len(sentence) + 2  # +2 for '. '
                if total >= max_chars:
                    break
            return '. '.join(seen.keys())[:max_chars]
        context = dedup_and_truncate(reranked_chunks, max_chars=800)

        if not context.strip() or ("apple" in context.lower() and "startup" in question.lower()):
            print("\n⚡ Using Gemini fallback!")
            return {"response": gemini_fallback(question)}

        prompt = prompt_builder.build_prompt(
            PromptType.RAG_FINANCIAL,
            question=question,
            context=context,
            config=PromptConfig()
        )
        print(f"Prompt length: {len(prompt)}")

        # Try Hugging Face LLM first, fallback to Gemini
        try:
            if llm is not None:
                print("🚀 Generating response with Hugging Face LLM...")
                response = llm.generate(prompt, max_tokens=200, temperature=0.1)
                answer = response["choices"][0]["text"].strip()
                print(f"✅ HF LLM response: {answer[:100]}...")
                print(f"⏱️ Response time: {response.get('response_time', 'N/A')}s")
            else:
                print("🔄 Hugging Face LLM not available, using Gemini fallback!")
                answer = gemini_fallback(question)
                    
        except Exception as e:
            print(f"\n⚠️ Hugging Face LLM failed: {e}, using Gemini fallback!")
            answer = gemini_fallback(question)

        return {"response": answer}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"❌ Failed to generate answer: {str(e)}"}


# ==== GET /ask (for testing) ====
@app.get("/ask")
async def ask_get(question: str):
    try:
        context_chunks = retriever.retrieve(question, k=1)
        context = "\n\n".join([chunk.page_content for chunk in context_chunks])

        prompt = prompt_builder.build_prompt(
            PromptType.RAG_FINANCIAL,
            question=question,
            context=context,
            config=PromptConfig()
        )
        
        # Try Hugging Face LLM first, fallback to Gemini
        try:
            if llm is not None:
                print("🚀 Generating response with Hugging Face LLM...")
                response = llm.generate(prompt, max_tokens=200, temperature=0.1)
                answer = response["choices"][0]["text"].strip()
                print(f"✅ HF LLM response: {answer[:100]}...")
            else:
                print("🔄 Hugging Face LLM not available, using Gemini fallback!")
                answer = gemini_fallback(question)
                    
        except Exception as e:
            print(f"\n⚠️ Hugging Face LLM failed: {e}, using Gemini fallback!")
            answer = gemini_fallback(question)

        return {"response": answer}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"❌ Failed to generate answer: {str(e)}"}


# ==== POST /chat (for frontend integration) ====
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        query = request.query
        print(f"\n💬 CHAT QUERY: {query}")
        
        # Use existing RAG pipeline
        context_chunks = retriever.retrieve(query, k=3)
        reranked_chunks = rerank(query, context_chunks, top_k=3)
        
        # Deduplicate and truncate context
        from collections import OrderedDict
        def dedup_and_truncate(chunks, max_chars=800):
            seen = OrderedDict()
            total = 0
            for chunk in chunks:
                for sentence in chunk.page_content.split('. '):
                    sentence = sentence.strip()
                    if sentence and sentence not in seen:
                        if total + len(sentence) + 2 > max_chars:
                            break
                        seen[sentence] = True
                        total += len(sentence) + 2  # +2 for '. '
                if total >= max_chars:
                    break
            return '. '.join(seen.keys())[:max_chars]
        
        context = dedup_and_truncate(reranked_chunks, max_chars=800)

        # If no context or specific conditions, use Gemini fallback
        if not context.strip():
            print("\n⚡ No context found, using Gemini fallback!")
            answer = gemini_fallback(query)
            return {"answer": answer}

        # Build prompt and generate response
        prompt = prompt_builder.build_prompt(
            PromptType.RAG_FINANCIAL,
            question=query,
            context=context,
            config=PromptConfig()
        )
        print(f"Prompt length: {len(prompt)}")

        # Try Hugging Face LLM first, fallback to Gemini
        try:
            if llm is not None:
                print("🚀 Generating response with Hugging Face LLM...")
                response = llm.generate(prompt, max_tokens=200, temperature=0.1)
                answer = response["choices"][0]["text"].strip()
                print(f"✅ HF LLM response: {answer[:100]}...")
                print(f"⏱️ Response time: {response.get('response_time', 'N/A')}s")
            else:
                print("🔄 Hugging Face LLM not available, using Gemini fallback!")
                answer = gemini_fallback(query)
                    
        except Exception as e:
            print(f"\n⚠️ Hugging Face LLM failed: {e}, using Gemini fallback!")
            answer = gemini_fallback(query)

        print(f"🎯 Final answer: {answer[:100]}...")
        return {"answer": answer}

    except Exception as e:
        import traceback
        traceback.print_exc()
        # Fallback to Gemini for any errors
        try:
            answer = gemini_fallback(request.query)
            return {"answer": answer}
        except:
            return {"answer": "❌ Sorry, I'm having trouble processing your request right now. Please try again."}


# ==== Health Check Endpoint ====
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "FinSight Copilot API",
        "llm_available": llm is not None,
        "gemini_configured": bool(GEMINI_API_KEY),
        "faiss_loaded": True
    }

# ==== Test Gemini Endpoint ====
@app.get("/test-gemini")
async def test_gemini():
    """Test if Gemini API is working"""
    try:
        test_question = "What is 2+2? Answer briefly."
        answer = gemini_fallback(test_question)
        return {
            "status": "success",
            "question": test_question,
            "answer": answer,
            "gemini_configured": bool(GEMINI_API_KEY)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "gemini_configured": bool(GEMINI_API_KEY)
        }

# ==== Upload Route ====
app.include_router(upload_router)

# ==== Chat History Route ====
app.include_router(chat_history_router)

# ==== Trading Route ====
app.include_router(trading_router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="debug")
