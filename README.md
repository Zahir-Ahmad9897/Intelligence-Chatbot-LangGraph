# 🤖 LangGraph Intelligence Chatbot

A professional, stateful AI Chatbot built using **LangGraph**, **LangChain**, and **Streamlit**. This project demonstrates advanced LLM orchestration with persistent memory, thread management, and a premium user interface.

## 🌟 Key Features

- **🧠 State Management**: Powered by LangGraph to maintain conversation flow and state transitions.
- **💾 Persistent Memory**: Supports multi-thread conversations. Switching between threads recovers the full context of that specific chat.
- **⚡ Real-time Streaming**: Seamless message streaming for a smooth, interactive experience.
- **📁 Thread History Sidebar**:
    - **New Chat**: Instantly start a fresh session with a unique Thread ID.
    - **Thread Switcher**: Browse and return to past conversations stored in memory.
    - **Manual ID Input**: Join specific sessions via custom Thread IDs.
- **🎨 Premium UI**: Modern, responsive design with dark mode support and intuitive controls.
- **🚀 High Performance**: Powered by **Groq (Llama 3.3-70b)** for lightning-fast inference.

## 🛠️ Tech Stack

- **Core**: Python 3.10+
- **Agent Framework**: [LangGraph](https://github.com/langchain-ai/langgraph)
- **LLM Framework**: [LangChain](https://github.com/langchain-ai/langchain)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Inference**: [Groq Cloud](https://groq.com/)
- **State Storage**: InMemorySaver (SQLite Persistence ready)

## 📁 Project Structure

```text
Chatbot/
├── chatbot_backend.py          # LangGraph graph definition and LLM logic
├── Chatbot_history_sidebar.py  # Main UI with history & thread management
├── chatbot_streaming_UI.py    # Alternative streaming-focused UI
├── requirements.txt            # Project dependencies
└── .env                       # API keys (Groq, etc.)
```

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have a Groq API Key. Get one at [console.groq.com](https://console.groq.com/).

### 2. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_gsk_api_key_here
```

### 4. Running the Application
Launch the professional interface with history management:
```bash
streamlit run Chatbot_history_sidebar.py
```

## 📈 Roadmap & Future Enhancements

- [ ] **SQL Persistence**: Replace InMemorySaver with SQLite for long-term database storage.
- [ ] **Tool Integration**: Add search capabilities and data analysis tools to the agent.
- [ ] **Multi-Agent Workflows**: Implement specialized nodes for research, coding, and summarization.
- [ ] **User Authentication**: Secure individual chat histories for different users.
- [ ] **Document Q&A**: RAG (Retrieval Augmented Generation) support for PDF/CSV files.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

---
*Built with ❤️ using LangGraph and Streamlit.*
