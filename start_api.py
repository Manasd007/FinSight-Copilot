#!/usr/bin/env python3
"""
Startup script for FinSight Copilot API
This script properly sets up the Python path and starts the API
"""

import sys
import os
import uvicorn

# Add backend to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

def start_api():
    """Start the FinSight Copilot API"""
    print("🚀 Starting FinSight Copilot API...")
    print(f"📁 Backend path: {backend_path}")
    print(f"🐍 Python path includes: {sys.path[:3]}...")
    
    # Start the API
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[backend_path]
    )

if __name__ == "__main__":
    start_api() 