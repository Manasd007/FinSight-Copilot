#!/usr/bin/env python3
"""
Local Hugging Face LLM Engine for FinSight Copilot
Uses Hugging Face models locally for faster inference
"""

import os
import time
from typing import Optional, Dict, Any
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LocalHuggingFaceEngine:
    """Local Hugging Face LLM Engine for fast inference"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"🚀 Initializing local Hugging Face model: {model_name}")
        print(f"💻 Using device: {self.device}")
        
        try:
            self._load_model()
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            print("💡 This model requires Hugging Face access. Using fallback.")
    
    def _load_model(self):
        """Load the model and tokenizer"""
        print("📥 Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            use_fast=False
        )
        
        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        print("📥 Loading model...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        if self.device == "cpu":
            self.model = self.model.to(self.device)
        
        print("✅ Model loaded successfully")
    
    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.3, 
                stop_sequences: Optional[list] = None) -> Dict[str, Any]:
        """
        Generate text using local Hugging Face model
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stop_sequences: Sequences to stop generation at
            
        Returns:
            Dictionary with generated text and metadata
        """
        try:
            if self.model is None or self.tokenizer is None:
                raise Exception("Model not loaded")
            
            # Format prompt for DialoGPT
            formatted_prompt = prompt
            
            # Tokenize input
            inputs = self.tokenizer(
                formatted_prompt,
                return_tensors="pt",
                truncation=True,
                max_length=2048
            ).to(self.device)
            
            print(f"🚀 Generating with local HF model...")
            start_time = time.time()
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Decode output
            generated_text = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            ).strip()
            
            return {
                "choices": [{
                    "text": generated_text,
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": inputs['input_ids'].shape[1],
                    "completion_tokens": len(outputs[0]) - inputs['input_ids'].shape[1],
                    "total_tokens": len(outputs[0])
                },
                "response_time": response_time
            }
                
        except Exception as e:
            print(f"❌ Local HF generation error: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test if model is loaded and working"""
        try:
            if self.model is None or self.tokenizer is None:
                print("❌ Model not loaded")
                return False
            
            # Simple test generation
            result = self.generate(
                prompt="Hello, how are you?",
                max_tokens=10,
                temperature=0.1
            )
            
            print("✅ Local HF model test successful")
            return True
            
        except Exception as e:
            print(f"❌ Local HF model test failed: {e}")
            return False

# Convenience function for easy integration
def get_local_hf_engine(model_name: str = "microsoft/DialoGPT-medium") -> LocalHuggingFaceEngine:
    """Get a local Hugging Face LLM engine instance"""
    return LocalHuggingFaceEngine(model_name)

# Test function
def test_local_hf_engine():
    """Test the local Hugging Face LLM engine"""
    print("🧪 Testing Local Hugging Face LLM Engine...")
    
    engine = LocalHuggingFaceEngine()
    
    if engine.test_connection():
        print("✅ Local HF engine test passed")
        
        # Test generation
        try:
            result = engine.generate(
                prompt="What is the capital of France?",
                max_tokens=20,
                temperature=0.1
            )
            print(f"✅ Generation test passed: {result['choices'][0]['text']}")
            print(f"⏱️ Response time: {result.get('response_time', 'N/A')}s")
        except Exception as e:
            print(f"❌ Generation test failed: {e}")
    else:
        print("❌ Local HF engine test failed")

if __name__ == "__main__":
    test_local_hf_engine() 