#!/usr/bin/env python3
"""
Test script to verify the new centralized path structure
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from backend.finsight_app.path_utils import (
    BASE_DIR, 
    DATA_DIR, 
    EMBEDDINGS_DIR, 
    LOGS_DIR, 
    MODELS_DIR,
    PROCESSED_DATA_DIR,
    SEC_FILINGS_DIR,
    STOCK_PRICES_DIR,
    get_faiss_index_dir,
    ensure_directories
)

def test_paths():
    """Test all path constants and ensure directories exist"""
    print("🔍 Testing FinSight Copilot Path Structure")
    print("=" * 60)
    
    # Test path constants
    paths_to_test = {
        "BASE_DIR": BASE_DIR,
        "DATA_DIR": DATA_DIR,
        "EMBEDDINGS_DIR": EMBEDDINGS_DIR,
        "LOGS_DIR": LOGS_DIR,
        "MODELS_DIR": MODELS_DIR,
        "PROCESSED_DATA_DIR": PROCESSED_DATA_DIR,
        "SEC_FILINGS_DIR": SEC_FILINGS_DIR,
        "STOCK_PRICES_DIR": STOCK_PRICES_DIR,
        "FAISS_INDEX_DIR": get_faiss_index_dir()
    }
    
    print("\n📁 Path Constants:")
    for name, path in paths_to_test.items():
        print(f"  {name}: {path}")
        if os.path.exists(path):
            print(f"    ✅ Exists")
        else:
            print(f"    ❌ Missing")
    
    # Ensure all directories exist
    print("\n🔧 Creating missing directories...")
    created_dirs = ensure_directories()
    print(f"✅ Created {len(created_dirs)} directories")
    
    # Test data directory contents
    print(f"\n📊 Data Directory Contents ({DATA_DIR}):")
    if os.path.exists(DATA_DIR):
        try:
            files = os.listdir(DATA_DIR)
            if files:
                for file in files[:10]:  # Show first 10 files
                    print(f"  📄 {file}")
                if len(files) > 10:
                    print(f"  ... and {len(files) - 10} more files")
            else:
                print("  📁 Directory is empty")
        except Exception as e:
            print(f"  ❌ Error reading directory: {e}")
    else:
        print("  ❌ Data directory does not exist")
    
    # Test embeddings directory
    print(f"\n🧠 Embeddings Directory Contents ({EMBEDDINGS_DIR}):")
    if os.path.exists(EMBEDDINGS_DIR):
        try:
            files = os.listdir(EMBEDDINGS_DIR)
            if files:
                for file in files:
                    print(f"  📄 {file}")
            else:
                print("  📁 Directory is empty")
        except Exception as e:
            print(f"  ❌ Error reading directory: {e}")
    else:
        print("  ❌ Embeddings directory does not exist")
    
    print("\n" + "=" * 60)
    print("✅ Path structure test completed!")

if __name__ == "__main__":
    test_paths() 