# FinSight Copilot 🤖📊

An intelligent financial analysis assistant that leverages RAG (Retrieval-Augmented Generation) to provide insights from financial reports, market data, and competitor analysis.

## 🎯 Project Overview

FinSight Copilot is designed to help financial professionals and analysts by:
- Analyzing 10-K/10-Q filings and financial reports
- Providing competitive intelligence and market insights
- Generating actionable recommendations for product improvements
- Offering real-time financial data analysis

## 📁 Project Structure

```
finsight-copilot/
│
├── data/                    # Raw financial reports, transcripts, scraped data
├── processed_data/          # Cleaned & chunked data
├── embeddings/              # FAISS or Chroma index
├── models/                  # Quantized LLMs or LoRA adapters
├── app/
│   ├── main.py              # Backend + RAG pipeline ✅
│   ├── prompts.py           # Prompt templates ✅
│   └── rag_utils.py         # Embedding, retrieval logic ✅
├── notebooks/               # Exploration, experiments, training
│   ├── fetch_stock_data.py  # Stock data collection ✅
│   ├── fetch_10k.py         # SEC filing downloader ✅
│   └── data_exploration.py  # Data analysis script ✅
├── ui/                      # Streamlit or CLI-based chat interface
│   └── app.py               # Streamlit UI ✅
├── requirements.txt         # Dependencies ✅
├── setup.py                 # Installation script ✅
├── env.example              # Environment template ✅
└── README.md                # Project overview ✅
```

## 🚦 Development Phases

### Phase 1: Project Setup + Data Collection (2-3 days) ✅ **COMPLETED**
- [x] Create project folder structure ✅
- [x] Install dependencies ✅
- [x] Create data collection scripts ✅
- [x] Build Streamlit UI ✅
- [x] Set up RAG pipeline foundation ✅
- [x] Create comprehensive prompt templates ✅

**🎉 Phase 1 Status: COMPLETE!** 

### Phase 2: Data Cleaning + Preprocessing (3-5 days) 🔄 **NEXT**
- [ ] Clean raw text data
- [ ] Chunk text into 512-1024 token segments
- [ ] Add metadata (source, date, type)
- [ ] Save processed data

### Phase 3: Embedding + Vector DB Setup (2-4 days)
- [ ] Generate embeddings using MiniLM or FinBERT
- [ ] Create FAISS/Chroma vector store
- [ ] Build retrieval function

### Phase 4: LLM Integration + RAG Pipeline (4-6 days)
- [ ] Set up prompt templates
- [ ] Load local quantized model
- [ ] Connect retriever + generator
- [ ] Create backend API

### Phase 5: Interface + Demo App (3-5 days)
- [ ] Build Streamlit UI
- [ ] Connect to RAG backend
- [ ] Add example prompts
- [ ] Upload functionality

### Phase 6: Fine-tuning (Optional - 5-7 days)
- [ ] Prepare training data
- [ ] Implement LoRA fine-tuning
- [ ] Train on phi-2 or tinyllama

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd finsight-copilot

# Run automated setup
python setup.py
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create environment file
cp env.example .env
# Edit .env with your API keys (optional)

# 3. Collect initial data
cd notebooks
python fetch_stock_data.py
python fetch_10k.py

# 4. Run the application
streamlit run ui/app.py
```

## 📊 Data Collection

The project includes automated data collection scripts:

### Stock Data Collection
```bash
cd notebooks
python fetch_stock_data.py
```
**Collects:**
- Historical stock prices (1 year)
- Company information and metrics
- Financial statements (income, balance sheet, cash flow)
- Market data for 25+ major companies

### SEC Filing Download
```bash
cd notebooks
python fetch_10k.py
```
**Downloads:**
- 10-K annual reports
- 10-Q quarterly reports
- Cleaned text versions
- Filing metadata

### Data Exploration
```bash
cd notebooks
python data_exploration.py
```
**Analyzes:**
- Performance metrics
- Data quality assessment
- Sector analysis
- Filing statistics

## 🛠️ Key Features

- **Intelligent Document Analysis**: Process and understand complex financial documents
- **Competitive Intelligence**: Analyze competitor positioning and market trends
- **Real-time Insights**: Get up-to-date financial data and analysis
- **Customizable Prompts**: Tailored prompts for different analysis types
- **Local Processing**: Run entirely on your machine for data privacy

## 📊 Data Sources

- **SEC EDGAR**: 10-K, 10-Q filings
- **Yahoo Finance**: Market data, financial summaries
- **Company Websites**: Product information, pricing
- **Financial News**: Market analysis and trends

## 🔧 Technical Stack

- **Backend**: Python, LangChain, Transformers
- **Vector Database**: FAISS/Chroma
- **Embeddings**: Sentence-Transformers, FinBERT
- **UI**: Streamlit, Gradio
- **Models**: Local quantized LLMs (llama.cpp, Hugging Face)

## 🔍 FAISS Index Management

All backend code uses a centralized utility function `get_faiss_index_dir()` (in `backend/finsight_app/path_utils.py`) to resolve the FAISS vector index directory:

- **Directory:** `embeddings/finsight_index/`
- **Index file:** `embeddings/finsight_index/index.faiss`
- **Chunk mapping:** `embeddings/finsight_index/chunk_mapping.pkl`

This ensures:
- No hardcoded or conflicting paths
- The app works from both the project root and backend/ directories
- Easy debugging and onboarding for new contributors

**Example usage:**
```python
from finsight_app.path_utils import get_faiss_index_dir
faiss_index_path = get_faiss_index_dir()
index_file_path = os.path.join(faiss_index_path, "index.faiss")
```

> Always use this utility for any code that reads or writes the FAISS index or chunk mapping files.

## 🎯 Current Capabilities

### ✅ What's Working Now
1. **Data Collection**: Automated stock data and SEC filing downloads
2. **Data Processing**: Text cleaning, chunking, and metadata extraction
3. **UI Framework**: Complete Streamlit interface with navigation
4. **RAG Foundation**: Embedding generation and retrieval system
5. **Prompt System**: Comprehensive templates for different analysis types

### 🔄 What's Next (Phase 2)
1. **Data Preprocessing**: Clean and chunk all collected documents
2. **Vector Database**: Create FAISS index for semantic search
3. **Model Integration**: Connect local LLM for generation
4. **End-to-End Testing**: Complete RAG pipeline validation

## 📈 Usage Examples

### CLI Interface
```bash
# General analysis
python app/main.py --query "Analyze Apple's competitive position" --type competitive

# Company-specific analysis
python app/main.py --company AAPL --type risk

# Process data
python app/main.py --process-data
```

### Web Interface
```bash
streamlit run ui/app.py
```
Then navigate to:
- **Overview**: Project status and features
- **Data Overview**: Dataset statistics and quality
- **Analysis**: Custom financial analysis queries
- **Quick Analysis**: Predefined analysis types
- **Data Collection**: Upload and manage data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for financial professionals**

### 🎉 Phase 1 Complete!
**Status**: ✅ All Phase 1 objectives achieved
**Next**: Ready to begin Phase 2 (Data Preprocessing)
**Timeline**: 2-3 days for Phase 2 completion 