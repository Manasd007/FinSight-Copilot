"""
FinSight Copilot - Setup Script
Helps with project installation and initial configuration
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install project dependencies"""
    print("📦 Installing dependencies...")
    
    # Upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "data",
        "processed_data", 
        "embeddings",
        "models",
        "logs",
        "notebooks",
        "ui"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def setup_environment():
    """Setup environment file"""
    print("⚙️ Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        # Copy example environment file
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your API keys if needed")
    else:
        print("ℹ️ Environment file already exists or template not found")
    
    return True

def download_sample_data():
    """Download sample data for testing"""
    print("📊 Downloading sample data...")
    
    try:
        # Import and run data collection scripts
        sys.path.append('notebooks')
        
        # Run stock data collection
        print("🔄 Collecting stock data...")
        from fetch_stock_data import StockDataCollector
        collector = StockDataCollector()
        collector.collect_default_dataset(period="6mo")  # Shorter period for testing
        
        # Run SEC filing download
        print("🔄 Downloading SEC filings...")
        from fetch_10k import SECFilingDownloader
        downloader = SECFilingDownloader()
        downloader.download_default_filings("10-K", limit=1)  # Limit for testing
        
        print("✅ Sample data downloaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading sample data: {e}")
        print("ℹ️ You can run data collection manually later")
        return False

def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import pandas as pd
        import yfinance as yf
        import streamlit as st
        from transformers import AutoTokenizer
        from sentence_transformers import SentenceTransformer
        
        print("✅ All core dependencies imported successfully")
        
        # Test basic functionality
        print("🔄 Testing basic functionality...")
        
        # Test yfinance
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        if info:
            print("✅ Yahoo Finance API working")
        
        # Test sentence transformers
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode("Test sentence")
        if len(embeddings) > 0:
            print("✅ Sentence transformers working")
        
        print("✅ Installation test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 FinSight Copilot Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("⚠️ Installation test failed, but setup completed")
    
    # Download sample data (optional)
    download_sample = input("\n📊 Download sample data for testing? (y/n): ").lower().strip()
    if download_sample in ['y', 'yes']:
        download_sample_data()
    
    print("\n🎉 FinSight Copilot setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys (optional)")
    print("2. Run the Streamlit UI: streamlit run ui/app.py")
    print("3. Or run the CLI: python app/main.py")
    print("4. Check the README.md for detailed usage instructions")
    
    print("\n🔗 Quick start commands:")
    print("  streamlit run ui/app.py          # Start web interface")
    print("  python app/main.py --help        # CLI help")
    print("  python notebooks/fetch_stock_data.py  # Collect stock data")
    print("  python notebooks/fetch_10k.py         # Download SEC filings")

if __name__ == "__main__":
    main() 