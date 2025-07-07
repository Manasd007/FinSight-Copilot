#!/usr/bin/env python3
"""
Hugging Face LLM Engine for FinSight Copilot
Uses Hugging Face Inference API for faster, scalable inference
"""

import os
import requests
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv('.env.local')

class HuggingFaceLLMEngine:
    """Hugging Face LLM Engine for remote inference"""
    
    def __init__(self, model_name: str = "meta-llama/Llama-2-7b-chat-hf"):
        self.model_name = model_name
        self.api_key = os.getenv("HF_API_KEY")
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        if not self.api_key:
            print("⚠️ HF_API_KEY not found in environment variables")
            print("💡 Set HF_API_KEY in your .env file for Hugging Face inference")
        
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
    
    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.3, 
                stop_sequences: Optional[list] = None) -> Dict[str, Any]:
        """
        Generate text using Hugging Face Inference API
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stop_sequences: Sequences to stop generation at
            
        Returns:
            Dictionary with generated text and metadata
        """
        try:
            if not self.api_key:
                raise Exception("HF_API_KEY not configured")
            
            # Prepare payload
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "do_sample": True,
                    "top_p": 0.9,
                    "return_full_text": False
                }
            }
            
            # Add stop sequences if provided
            if stop_sequences:
                payload["parameters"]["stop"] = stop_sequences
            
            print(f"🚀 Calling Hugging Face API: {self.model_name}")
            start_time = time.time()
            
            # Make API call
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60  # 60 second timeout
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract generated text
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                else:
                    generated_text = result.get('generated_text', '')
                
                return {
                    "choices": [{
                        "text": generated_text,
                        "finish_reason": "stop"
                    }],
                    "usage": {
                        "prompt_tokens": len(prompt.split()),
                        "completion_tokens": len(generated_text.split()),
                        "total_tokens": len(prompt.split()) + len(generated_text.split())
                    },
                    "response_time": response_time
                }
            else:
                error_msg = f"HF API Error {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            print("⏰ Hugging Face API timeout")
            raise Exception("Hugging Face API timeout")
        except requests.exceptions.RequestException as e:
            print(f"❌ Hugging Face API request error: {e}")
            raise Exception(f"Hugging Face API error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error in HF LLM engine: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test if Hugging Face API is accessible"""
        try:
            if not self.api_key:
                print("❌ HF_API_KEY not configured")
                return False
            
            # Simple test call
            test_payload = {
                "inputs": "Hello, how are you?",
                "parameters": {
                    "max_new_tokens": 10,
                    "temperature": 0.1
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=test_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ Hugging Face API connection successful")
                return True
            else:
                print(f"❌ Hugging Face API test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Hugging Face API test error: {e}")
            return False

# Convenience function for easy integration
def get_hf_llm_engine(model_name: str = "meta-llama/Llama-2-7b-chat-hf") -> HuggingFaceLLMEngine:
    """Get a Hugging Face LLM engine instance"""
    return HuggingFaceLLMEngine(model_name)

# Test function
def test_hf_engine():
    """Test the Hugging Face LLM engine"""
    print("🧪 Testing Hugging Face LLM Engine...")
    
    engine = HuggingFaceLLMEngine()
    
    if engine.test_connection():
        print("✅ Connection test passed")
        
        # Test generation
        try:
            result = engine.generate(
                prompt="What is the capital of France?",
                max_tokens=20,
                temperature=0.1
            )
            print(f"✅ Generation test passed: {result['choices'][0]['text']}")
        except Exception as e:
            print(f"❌ Generation test failed: {e}")
    else:
        print("❌ Connection test failed")

if __name__ == "__main__":
    test_hf_engine() 