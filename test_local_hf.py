#!/usr/bin/env python3
"""
Test Local Hugging Face Engine
"""

import sys
import os

# Add backend to path
sys.path.insert(0, 'backend')

def test_local_hf_engine():
    """Test the local Hugging Face engine"""
    print("🧪 Testing Local Hugging Face Engine...")
    print("🚀 Using open model: microsoft/DialoGPT-medium")
    
    try:
        from finsight_app.local_hf_engine import LocalHuggingFaceEngine
        
        # Initialize engine with open model
        engine = LocalHuggingFaceEngine("microsoft/DialoGPT-medium")
        
        # Test connection
        if engine.test_connection():
            print("✅ Local HF engine test passed")
            
            # Test generation
            try:
                result = engine.generate(
                    prompt="What is the capital of France? Answer briefly.",
                    max_tokens=20,
                    temperature=0.1
                )
                print(f"✅ Generation test passed: {result['choices'][0]['text']}")
                print(f"⏱️ Response time: {result.get('response_time', 'N/A')}s")
                return True
            except Exception as e:
                print(f"❌ Generation test failed: {e}")
                return False
        else:
            print("❌ Local HF engine test failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_local_hf_engine() 