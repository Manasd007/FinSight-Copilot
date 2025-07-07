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
├── backend/                 # FastAPI backend with RAG pipeline ✅
│   ├── main.py              # Main FastAPI application ✅
│   ├── finsight_app/        # Core RAG and LLM modules ✅
│   │   ├── prompts.py       # Financial analysis prompts ✅
│   │   ├── rag_utils.py     # RAG pipeline utilities ✅
│   │   ├── llm_engine.py    # LLM integration ✅
│   │   └── path_utils.py    # Path management ✅
│   ├── embeddings/          # FAISS vector index ✅
│   └── data/                # Financial data and SEC filings ✅
├── frontend/                # React + TypeScript frontend ✅
│   ├── src/                 # React components ✅
│   │   ├── pages/           # Page components ✅
│   │   ├── components/      # UI components ✅
│   │   └── services/        # API services ✅
│   └── package.json         # Frontend dependencies ✅
├── data/                    # Raw financial data ✅
├── models/                  # LLaMA model files ✅
├── logs/                    # Application logs ✅
├── requirements.txt         # Python dependencies ✅
├── start_api.py             # Backend startup script ✅
├── env.example              # Environment template ✅
└── README.md                # Project documentation ✅
```

## 🚦 Development Phases

### Phase 1: Project Setup + Data Collection ✅ **COMPLETED**
- [x] Create project folder structure ✅
- [x] Install dependencies ✅
- [x] Create data collection scripts ✅
- [x] Set up RAG pipeline foundation ✅
- [x] Create comprehensive prompt templates ✅

### Phase 2: Backend Development ✅ **COMPLETED**
- [x] FastAPI backend with RAG pipeline ✅
- [x] LLaMA model integration with timeout handling ✅
- [x] Gemini API fallback for reliability ✅
- [x] FAISS vector database setup ✅
- [x] Financial data processing and embedding ✅

### Phase 3: Frontend Development ✅ **COMPLETED**
- [x] React + TypeScript frontend ✅
- [x] Modern chat interface ✅
- [x] Real-time communication with backend ✅
- [x] Responsive design ✅

### Phase 4: Integration & Testing ✅ **COMPLETED**
- [x] End-to-end RAG pipeline ✅
- [x] Error handling and fallbacks ✅
- [x] Performance optimization ✅
- [x] Production-ready deployment ✅

**🎉 All Phases Complete! FinSight Copilot is fully functional!**

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)
- LLaMA model file (download separately)

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/Manasd007/FinSight-Copilot.git
cd FinSight-Copilot

# Install Python dependencies
pip install -r requirements.txt

# Set up environment (optional - for Gemini fallback)
cp env.example .env
# Edit .env with your GEMINI_API_KEY (optional)

# Start the backend server
python start_api.py
```

### Frontend Setup
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install frontend dependencies
npm install

# Start the frontend development server
npm run dev
```

### Access the Application
- **Backend API**: http://127.0.0.1:8000
- **Frontend**: http://localhost:8080
- **API Documentation**: http://127.0.0.1:8000/docs

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

- **Backend**: FastAPI, Python, LangChain, Transformers
- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Vector Database**: FAISS
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **LLMs**: LLaMA-2-7B (local) + Gemini 1.5 Flash (fallback)
- **Reranking**: Cross-Encoder (qnli-distilroberta-base)
- **Data**: SEC EDGAR filings, Financial reports

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
1. **Complete RAG Pipeline**: End-to-end retrieval and generation system ✅
2. **FastAPI Backend**: Production-ready API with proper error handling ✅
3. **React Frontend**: Modern chat interface with real-time responses ✅
4. **LLaMA Integration**: Local model with intelligent timeout handling ✅
5. **Gemini Fallback**: Reliable API fallback when LLaMA is slow ✅
6. **Financial Data**: Pre-processed SEC filings and financial reports ✅
7. **Vector Search**: FAISS-based semantic search for relevant context ✅

### 🚀 Key Features
- **Intelligent Financial Analysis**: Ask questions about company financials
- **Real-time Responses**: Get instant answers with context from SEC filings
- **Reliable Performance**: Automatic fallback ensures responses even if local model is slow
- **Modern UI**: Clean, responsive chat interface
- **Production Ready**: Proper error handling, logging, and deployment setup

## 📈 Usage Examples

### Web Interface (Recommended)
1. **Start the backend**: `python start_api.py`
2. **Start the frontend**: `cd frontend && npm run dev`
3. **Open browser**: Navigate to http://localhost:8080
4. **Ask questions** like:
   - "What is Apple's Q3 2023 revenue?"
   - "What are the main risks mentioned in Microsoft's 10-K?"
   - "How does Tesla's financial performance compare to competitors?"

### API Endpoints
```bash
# Chat endpoint
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Apple\'s revenue?"}'

# Test Gemini endpoint
curl "http://127.0.0.1:8000/test-gemini"

# API documentation
# Visit: http://127.0.0.1:8000/docs
```

### Example Questions
- **Financial Analysis**: "What was Apple's net income in 2023?"
- **Risk Assessment**: "What risks does Microsoft mention in their filings?"
- **Competitive Analysis**: "How does Tesla compare to traditional automakers?"
- **Market Trends**: "What are the key trends in the tech industry?"

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

### 🎉 Project Complete!
**Status**: ✅ All phases completed successfully
**Features**: Full RAG pipeline with modern UI
**Ready for**: Production deployment and further enhancements 