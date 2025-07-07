# 🚀 FinSight Copilot

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-blue)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/frontend-React-blue)](https://react.dev/)
[![RAG](https://img.shields.io/badge/AI-RAG-yellow)](https://github.com/Manasd007/FinSight-Copilot)

> **Your AI-powered financial analysis assistant.**

---

## ✨ Overview

**FinSight Copilot** is an intelligent assistant for financial professionals, leveraging Retrieval-Augmented Generation (RAG) to analyze SEC filings, financial data, and market trends. It delivers actionable insights, competitive intelligence, and real-time answers—all with a modern chat UI.

---

## 🏗️ Project Structure

```
finsight-copilot/
├── backend/      # FastAPI backend (RAG, LLM, data)
├── frontend/     # React + TypeScript frontend
├── data/         # Raw & processed financial data
├── models/       # LLaMA model files
├── requirements.txt
├── env.example
└── README.md
```

---

## ⚡ Quickstart

### Prerequisites
- Python 3.9+
- Node.js 16+
- LLaMA model (optional, for local LLM)

### 1. Backend
```sh
git clone https://github.com/Manasd007/FinSight-Copilot.git
cd FinSight-Copilot
pip install -r requirements.txt
cp env.example .env  # (Optional: add GEMINI_API_KEY)
cd backend
uvicorn main:app
```

### 2. Frontend
```sh
cd frontend
npm install
npm run dev
```

- **Backend**: http://127.0.0.1:8000
- **Frontend**: http://localhost:8080
- **API Docs**: http://127.0.0.1:8000/docs

---

## 🌟 Features

- **RAG Pipeline**: Combines retrieval and generation for context-rich answers
- **SEC Filings Analysis**: Deep-dive into 10-K/10-Q reports
- **Competitive Intelligence**: Compare companies and market trends
- **Real-time Data**: Up-to-date financials and insights
- **Modern Chat UI**: Responsive, intuitive frontend
- **LLM Flexibility**: Local LLaMA-2-7B or Gemini API fallback
- **FAISS Vector Search**: Fast, semantic retrieval
- **Production Ready**: Error handling, logging, and robust deployment

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python, LangChain, Transformers, FAISS
- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **LLMs**: LLaMA-2-7B (local), Gemini 1.5 Flash (fallback)
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **Reranker**: Cross-Encoder (qnli-distilroberta-base)

---

## 📈 Usage Examples

- "What is Apple's Q3 2023 revenue?"
- "Main risks in Microsoft's 10-K?"
- "Compare Tesla's financials to competitors."

### API Example
```sh
curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d '{"query": "What is Apple revenue?"}'
```

---

## 🤝 Contributing

1. Fork & clone
2. Create a feature branch
3. Make changes & add tests
4. Submit a pull request

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.

---

**Built with ❤️ for financial professionals.** 