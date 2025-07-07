#!/usr/bin/env python3
"""
Deploy FinSight Copilot to Hugging Face
This script helps you deploy your model and set up the inference endpoint
"""

import os
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "transformers",
        "torch", 
        "huggingface_hub",
        "requests"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def setup_huggingface_login():
    """Set up Hugging Face login"""
    print("\n🔐 Setting up Hugging Face login...")
    
    # Check if already logged in
    try:
        result = subprocess.run(["huggingface-cli", "whoami"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Already logged in as: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("❌ huggingface-cli not found")
        return False
    
    # Prompt for login
    print("💡 Please run: huggingface-cli login")
    print("💡 Get your token from: https://huggingface.co/settings/tokens")
    
    token = input("Enter your Hugging Face token (or press Enter to skip): ").strip()
    if token:
        try:
            subprocess.run(["huggingface-cli", "login", "--token", token], check=True)
            print("✅ Hugging Face login successful")
            return True
        except subprocess.CalledProcessError:
            print("❌ Hugging Face login failed")
            return False
    else:
        print("⚠️ Skipping Hugging Face login")
        return False

def convert_model():
    """Convert GGUF model to Hugging Face format"""
    print("\n🔄 Converting model to Hugging Face format...")
    
    model_path = "models/llama-2-7b-chat.Q2_K.gguf"
    output_dir = "huggingface-model/llama-2-7b-finsight"
    
    if not os.path.exists(model_path):
        print(f"❌ Model not found at: {model_path}")
        print("💡 Please download the LLaMA model first")
        return False
    
    try:
        subprocess.run([
            "python", "convert_llama_weights.py",
            "--input_path", model_path,
            "--output_dir", output_dir,
            "--model_size", "7B"
        ], check=True)
        
        print(f"✅ Model converted to: {output_dir}")
        return True
    except subprocess.CalledProcessError:
        print("❌ Model conversion failed")
        return False

def push_to_hub():
    """Push model to Hugging Face Hub"""
    print("\n📤 Pushing model to Hugging Face Hub...")
    
    model_dir = "huggingface-model/llama-2-7b-finsight"
    repo_name = "Manasd007/llama-2-7b-finsight"
    
    if not os.path.exists(model_dir):
        print(f"❌ Model directory not found: {model_dir}")
        return False
    
    try:
        # Push model
        subprocess.run([
            "huggingface-cli", "upload",
            repo_name,
            model_dir,
            "--repo-type", "model"
        ], check=True)
        
        print(f"✅ Model pushed to: https://huggingface.co/{repo_name}")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to push model to Hub")
        return False

def create_inference_endpoint():
    """Create Hugging Face Inference Endpoint"""
    print("\n🚀 Setting up Inference Endpoint...")
    print("📋 Manual steps required:")
    print("1. Go to: https://huggingface.co/inference-endpoints")
    print("2. Click 'New Endpoint'")
    print("3. Select model: Manasd007/llama-2-7b-finsight")
    print("4. Choose hardware: CPU (free) or GPU (paid)")
    print("5. Set environment: Transformers")
    print("6. Click 'Deploy'")
    print("\n💡 Your endpoint URL will be:")
    print("https://api-inference.huggingface.co/models/Manasd007/llama-2-7b-finsight")

def update_backend_config():
    """Update backend configuration for Hugging Face"""
    print("\n⚙️ Updating backend configuration...")
    
    # Check if .env file exists
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"⚠️ {env_file} not found, creating from template...")
        subprocess.run(["cp", "env.example", env_file])
    
    print("✅ Backend configuration updated")
    print("💡 Don't forget to:")
    print("   - Set HF_API_KEY in your .env file")
    print("   - Restart your backend server")

def main():
    """Main deployment function"""
    print("🚀 FinSight Copilot - Hugging Face Deployment")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        return
    
    # Setup login
    if not setup_huggingface_login():
        print("\n⚠️ Hugging Face login required for deployment")
        return
    
    # Convert model
    if not convert_model():
        print("\n❌ Model conversion failed")
        return
    
    # Push to hub
    if not push_to_hub():
        print("\n❌ Failed to push model to Hub")
        return
    
    # Create endpoint
    create_inference_endpoint()
    
    # Update config
    update_backend_config()
    
    print("\n🎉 Deployment setup complete!")
    print("\n📋 Next steps:")
    print("1. Set up your inference endpoint (manual)")
    print("2. Add HF_API_KEY to your .env file")
    print("3. Restart your backend: python start_api.py")
    print("4. Test the new Hugging Face integration")

if __name__ == "__main__":
    main() 