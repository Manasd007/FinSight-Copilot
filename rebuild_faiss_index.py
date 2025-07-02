#!/usr/bin/env python3
"""
Rebuild FAISS Index Script
This script rebuilds the FAISS index using the existing chunk mapping
and chunk text files to ensure proper LangChain compatibility.
"""

import pickle
import os
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

def rebuild_faiss_index():
    """Rebuild the FAISS index using existing chunk mapping and chunk files"""
    
    print("🔧 Rebuilding FAISS Index...")
    
    # Paths
    chunk_mapping_path = "./embeddings/chunk_mapping.pkl"
    processed_data_dir = "./processed_data"
    faiss_output_path = "./embeddings/finsight_index.faiss"
    
    # Check if chunk mapping exists
    if not os.path.exists(chunk_mapping_path):
        print(f"❌ Chunk mapping not found at {chunk_mapping_path}")
        return False
    
    try:
        # Load chunk mapping
        print("📖 Loading chunk mapping...")
        with open(chunk_mapping_path, "rb") as f:
            chunk_mapping = pickle.load(f)
        
        print(f"📊 Found {len(chunk_mapping)} chunks")
        
        # Convert to Document objects
        print("🔄 Reading chunk files and converting to Document objects...")
        documents = []
        missing_files = 0
        for entry in chunk_mapping:
            company = entry.get('company', 'unknown')
            file_name = entry.get('file')
            if not file_name:
                continue
            chunk_path = os.path.join(processed_data_dir, file_name)
            if not os.path.exists(chunk_path):
                print(f"⚠️ Missing chunk file: {chunk_path}")
                missing_files += 1
                continue
            with open(chunk_path, 'r', encoding='utf-8') as cf:
                chunk_text = cf.read()
            doc = Document(
                page_content=chunk_text,
                metadata={
                    'company': company,
                    'file': file_name
                }
            )
            documents.append(doc)
        print(f"✅ Loaded {len(documents)} chunk files. Missing: {missing_files}")
        
        # Initialize embedding model
        print("🤖 Initializing embedding model...")
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Create FAISS vectorstore
        print("🏗️ Creating FAISS vectorstore...")
        vectorstore = FAISS.from_documents(documents, embedding_model)
        
        # Save the vectorstore properly
        print(f"💾 Saving vectorstore to {faiss_output_path}...")
        vectorstore.save_local(faiss_output_path)
        
        # Verify the files were created
        index_faiss_path = os.path.join(faiss_output_path, "index.faiss")
        index_pkl_path = os.path.join(faiss_output_path, "index.pkl")
        
        if os.path.exists(index_faiss_path) and os.path.exists(index_pkl_path):
            print("✅ FAISS index rebuilt successfully!")
            print(f"   - index.faiss: {os.path.getsize(index_faiss_path)} bytes")
            print(f"   - index.pkl: {os.path.getsize(index_pkl_path)} bytes")
            
            # Test loading
            print("🧪 Testing index loading...")
            test_vectorstore = FAISS.load_local(faiss_output_path, embedding_model, allow_dangerous_deserialization=True)
            print(f"✅ Index loaded successfully! Total documents: {test_vectorstore.index.ntotal}")
            
            return True
        else:
            print("❌ Failed to create required files")
            return False
            
    except Exception as e:
        print(f"❌ Error rebuilding FAISS index: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = rebuild_faiss_index()
    if success:
        print("\n🎉 FAISS index rebuild completed successfully!")
        print("You can now restart your FastAPI application.")
    else:
        print("\n💥 FAISS index rebuild failed!")
        print("Please check the error messages above.") 