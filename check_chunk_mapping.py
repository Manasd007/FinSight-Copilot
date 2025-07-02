#!/usr/bin/env python3
"""
Check Chunk Mapping Structure
This script inspects the chunk mapping file to understand its format.
"""

import pickle
import os

def check_chunk_mapping():
    """Check the structure of the chunk mapping file"""
    
    chunk_mapping_path = "./embeddings/chunk_mapping.pkl"
    
    if not os.path.exists(chunk_mapping_path):
        print(f"❌ Chunk mapping not found at {chunk_mapping_path}")
        return
    
    try:
        with open(chunk_mapping_path, "rb") as f:
            chunk_mapping = pickle.load(f)
        
        print(f"📊 Chunk mapping type: {type(chunk_mapping)}")
        print(f"📊 Chunk mapping length: {len(chunk_mapping)}")
        
        if isinstance(chunk_mapping, list):
            print("📋 It's a list!")
            if len(chunk_mapping) > 0:
                print(f"📋 First item type: {type(chunk_mapping[0])}")
                print(f"📋 First item keys: {list(chunk_mapping[0].keys())}")
                for k, v in chunk_mapping[0].items():
                    print(f"    Key: {k} | Value (first 200 chars): {str(v)[:200]}")
        elif isinstance(chunk_mapping, dict):
            print("📋 It's a dictionary!")
            print(f"📋 Keys: {list(chunk_mapping.keys())[:5]}...")  # Show first 5 keys
            if chunk_mapping:
                first_key = list(chunk_mapping.keys())[0]
                print(f"📋 First value: {chunk_mapping[first_key][:200]}...")
        
    except Exception as e:
        print(f"❌ Error reading chunk mapping: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_chunk_mapping() 