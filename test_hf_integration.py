#!/usr/bin/env python3
"""
Test Hugging Face Integration for FinSight Copilot
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv('.env.local')

def test_hf_engine():
    """Test the Hugging Face LLM engine"""
    print("🧪 Testing Hugging Face LLM Engine...")
    
    try:
        from backend.finsight_app.hf_llm_engine import HuggingFaceLLMEngine
        
        # Initialize engine
        engine = HuggingFaceLLMEngine("meta-llama/Llama-2-7b-chat-hf")
        
        # Test connection
        if engine.test_connection():
            print("✅ Connection test passed")
            
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
            print("❌ Connection test failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_backend_integration():
    """Test backend integration with Hugging Face"""
    print("\n🧪 Testing Backend Integration...")
    
    try:
        # Import backend modules
        sys.path.insert(0, 'backend')
        from main import app
        
        print("✅ Backend imports successful")
        
        # Test if Hugging Face engine is initialized
        from finsight_app.hf_llm_engine import HuggingFaceLLMEngine
        
        # This would normally be done in the main app
        print("✅ Hugging Face engine can be imported")
        return True
        
    except ImportError as e:
        print(f"❌ Backend import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Backend integration error: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n🧪 Testing Environment Configuration...")
    
    # Check API keys
    hf_api_key = os.getenv("HF_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if hf_api_key:
        print(f"✅ HF_API_KEY configured: {hf_api_key[:10]}...")
    else:
        print("⚠️ HF_API_KEY not configured")
    
    if gemini_api_key:
        print(f"✅ GEMINI_API_KEY configured: {gemini_api_key[:10]}...")
    else:
        print("⚠️ GEMINI_API_KEY not configured")
    
    return bool(hf_api_key or gemini_api_key)

def main():
    """Main test function"""
    print("🚀 FinSight Copilot - Hugging Face Integration Test")
    print("=" * 60)
    
    # Test environment
    env_ok = test_environment()
    
    # Test HF engine
    hf_ok = test_hf_engine()
    
    # Test backend integration
    backend_ok = test_backend_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"Environment: {'✅' if env_ok else '❌'}")
    print(f"Hugging Face Engine: {'✅' if hf_ok else '❌'}")
    print(f"Backend Integration: {'✅' if backend_ok else '❌'}")
    
    if all([env_ok, hf_ok, backend_ok]):
        print("\n🎉 All tests passed! Hugging Face integration is ready!")
        print("\n💡 Next steps:")
        print("1. Start your backend: python start_api.py")
        print("2. Test with a question in your frontend")
        print("3. Monitor response times and performance")
    else:
        print("\n⚠️ Some tests failed. Please check the configuration.")
        print("\n💡 Troubleshooting:")
        if not env_ok:
            print("- Set HF_API_KEY in your .env file")
        if not hf_ok:
            print("- Check your Hugging Face model deployment")
        if not backend_ok:
            print("- Ensure all dependencies are installed")

if __name__ == "__main__":
    main() 