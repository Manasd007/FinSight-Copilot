#!/usr/bin/env python3
"""
Test which model is being used (Hugging Face vs Gemini)
"""

import requests
import json

def test_model_source():
    """Test which model is being used"""
    print("🧪 Testing Model Source...")
    
    # Test question that should trigger local model
    test_question = "What is 2+2? Answer in one word only."
    
    try:
        # Make request to /ask endpoint
        response = requests.post(
            "http://localhost:8000/ask",
            json={"question": test_question},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get("response", "")
            print(f"✅ Response: {answer}")
            print(f"📝 Response length: {len(answer)}")
            
            # Analyze response characteristics
            if len(answer) < 50 and "4" in answer:
                print("🎯 Likely Hugging Face model (short, direct answer)")
            elif len(answer) > 100 and ("Here's" in answer or "Let me" in answer):
                print("🎯 Likely Gemini model (detailed, explanatory)")
            else:
                print("🤔 Uncertain model source")
                
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_model_source() 