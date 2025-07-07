#!/usr/bin/env python3
"""
Test Financial Knowledge Span
Tests the system with various financial questions to check knowledge coverage
"""

import requests
import json
import time

def test_financial_knowledge():
    """Test various financial questions to check knowledge span"""
    print("🧪 Testing Financial Knowledge Span...")
    print("=" * 60)
    
    # Test questions covering different aspects
    test_questions = [
        # Basic company info
        "What is Apple's market cap?",
        "What is Tesla's revenue in 2023?",
        "What is Microsoft's stock price?",
        
        # Financial metrics
        "What is Apple's P/E ratio?",
        "What is Tesla's debt-to-equity ratio?",
        "What is Microsoft's profit margin?",
        
        # Specific financial data
        "What was Apple's Q4 2023 revenue?",
        "What is Tesla's cash flow from operations?",
        "What is Microsoft's total assets?",
        
        # Complex financial analysis
        "Compare Apple and Microsoft's financial performance",
        "What are the main risks for Tesla?",
        "How does Apple's financial health compare to competitors?",
        
        # Edge cases
        "What is the revenue of a company called XYZ Corp?",
        "What is the stock price of a non-existent company?",
        "What are the financials of a startup that doesn't exist?"
    ]
    
    results = []
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 40)
        
        try:
            start_time = time.time()
            
            response = requests.post(
                "http://localhost:8000/ask",
                json={"question": question},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("response", "")
                
                print(f"✅ Response: {answer[:200]}...")
                print(f"⏱️ Response time: {response_time:.2f}s")
                print(f"📏 Answer length: {len(answer)} chars")
                
                # Analyze response quality
                if len(answer) > 50:
                    print("🎯 Response quality: Detailed")
                elif len(answer) > 20:
                    print("🎯 Response quality: Moderate")
                else:
                    print("🎯 Response quality: Brief")
                    
                results.append({
                    "question": question,
                    "answer": answer,
                    "response_time": response_time,
                    "length": len(answer),
                    "status": "success"
                })
                
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(response.text)
                results.append({
                    "question": question,
                    "status": "failed",
                    "error": f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "question": question,
                "status": "error",
                "error": str(e)
            })
        
        # Small delay between requests
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 KNOWLEDGE SPAN TEST SUMMARY")
    print("=" * 60)
    
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]
    
    print(f"✅ Successful responses: {len(successful)}/{len(results)}")
    print(f"❌ Failed responses: {len(failed)}/{len(results)}")
    
    if successful:
        avg_response_time = sum(r["response_time"] for r in successful) / len(successful)
        avg_length = sum(r["length"] for r in successful) / len(successful)
        print(f"⏱️ Average response time: {avg_response_time:.2f}s")
        print(f"📏 Average answer length: {avg_length:.0f} chars")
    
    print("\n🎯 Knowledge Coverage Analysis:")
    print("- Basic company info: Should work well")
    print("- Financial metrics: Should work if in database")
    print("- Complex analysis: May use Gemini fallback")
    print("- Edge cases: Should handle gracefully")

if __name__ == "__main__":
    test_financial_knowledge() 