# main.py
# FinSight Copilot - Main Application
# RAG-based financial analysis assistant (FastAPI backend)

from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from finsight_app.prompts import FinSightPrompts, PromptType, PromptConfig
from finsight_app.rag_utils import RetrievalSystem
from fastapi.middleware.cors import CORSMiddleware
# ==== FastAPI Init ====
app = FastAPI()
app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Or ["http://localhost:3000"] for more security
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
# ==== Load FAISS vectorstore ===
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
faiss_index_path = "./embeddings/finsight_index.faiss"
retriever = RetrievalSystem(
    vectorstore=FAISS.load_local(faiss_index_path, embeddings=embedding_model, allow_dangerous_deserialization=True)
)

# ==== Load local LLaMA model ===
llm = Llama(
    model_path="./models/llama-2-7b-chat.Q2_K.gguf",
    n_ctx=2048,
    n_threads=8,
    temperature=0.3
)

prompt_builder = FinSightPrompts()

# ==== Request Schema ====
class AskRequest(BaseModel):
    question: str

# ==== /ask Endpoint (POST) ====
@app.post("/ask")
async def ask(request: AskRequest):
    try:
        question = request.question
        print(f"Received question: {question}")
        
        # Step 1: Retrieve context
        print("Retrieving context...")
        context_chunks = retriever.retrieve(question, k=1)  # Reduced to 1 for faster testing
        if isinstance(context_chunks, list):
            context = "\n\n".join([chunk.page_content if hasattr(chunk, 'page_content') else str(chunk) for chunk in context_chunks])
        else:
            context = str(context_chunks)
        
        # Truncate context if too long (rough estimate: 1 token ≈ 4 characters)
        max_context_chars = 800  # Reduced for faster testing
        if len(context) > max_context_chars:
            context = context[:max_context_chars] + "..."
        
        print(f"Retrieved context length: {len(context)}")

        # Step 2: Build prompt
        print("Building prompt...")
        prompt = prompt_builder.build_prompt(
            PromptType.RAG_FINANCIAL,
            question=question,
            context=context,
            config=PromptConfig()
        )
        print(f"Prompt length: {len(prompt)}")

        # Step 3: Generate response
        print("Generating response...")
        response = llm(prompt, max_tokens=200, stop=["</s>"])["choices"][0]["text"]  # Reduced to 200 tokens
        print("Response generated successfully")
        return {"response": response.strip()}
    except Exception as e:
        print(f"Error in ask (POST): {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

# ==== /ask Endpoint (GET) for easier testing ====
@app.get("/ask")
async def ask_get(question: str):
    try:
        print(f"Received question: {question}")
        
        # Step 1: Retrieve context
        print("Retrieving context...")
        context_chunks = retriever.retrieve(question, k=1)  # Reduced to 1 for faster testing
        if isinstance(context_chunks, list):
            context = "\n\n".join([chunk.page_content if hasattr(chunk, 'page_content') else str(chunk) for chunk in context_chunks])
        else:
            context = str(context_chunks)
        
        # Truncate context if too long (rough estimate: 1 token ≈ 4 characters)
        max_context_chars = 800  # Reduced for faster testing
        if len(context) > max_context_chars:
            context = context[:max_context_chars] + "..."
        
        print(f"Retrieved context length: {len(context)}")

        # Step 2: Build prompt
        print("Building prompt...")
        prompt = prompt_builder.build_prompt(
            PromptType.RAG_FINANCIAL,
            question=question,
            context=context,
            config=PromptConfig()
        )
        
        print(f"Prompt length: {len(prompt)}")

        # Step 3: Generate response
        print("Generating response...")
        response = llm(prompt, max_tokens=200, stop=["</s>"])["choices"][0]["text"]  # Reduced to 200 tokens
        
        print("Response generated successfully")
        return {"response": response.strip()}
        
    except Exception as e:
        print(f"Error in ask_get: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
