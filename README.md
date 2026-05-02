# 🤖 Agentic AI Chatbot

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/orchestration-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![LangSmith](https://img.shields.io/badge/Observability-LangSmith-green.svg)](https://smith.langchain.com/)

A production-ready, state-aware AI chatbot built with **LangGraph**, **Groq (Llama 3.3)**, and **Streamlit**.

## ✨ Features
- **🧠 LangGraph Orchestration**: Complex, stateful conversation flows.
- **💾 SQLite Memory**: Chat threads are automatically saved and instantly recoverable.
- **⚡ Real-time Streaming**: Ultra low-latency responses via Groq's LPUs.
- **📊 LangSmith Observability**: Full telemetry and UUIDv7 thread tracking.

## 🚀 Quick Start

**1. Clone & Install**
```bash
git clone https://github.com/Zahir-Ahmad9897/Intelligence-Chatbot-LangGraph.git
cd Intelligence-Chatbot-LangGraph/Chatbot
pip install -r requirements.txt
```

**2. Set Environment Variables (`.env`)**
```env
GROQ_API_KEY="your_groq_key"
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="your_langsmith_key"
LANGCHAIN_PROJECT="Smart Chatbot"
```

**3. Run Application**
```bash
streamlit run app.py
```

## 📁 Repository Structure
- `app.py`: Streamlit Frontend
- `backend.py`: LangGraph & SQLite Backend
- `historical_versions/`: Step-by-step scripts demonstrating my progression from a basic UI to advanced orchestration.
