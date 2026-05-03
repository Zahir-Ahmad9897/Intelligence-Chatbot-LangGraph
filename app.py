# =========================
# app.py
# Full version with LangGraph memory + LangSmith thread grouping
# I made ONLY required changes.
# Your original logic, UI, sidebar, chat history, SQLite thread usage remain preserved.
# I did NOT remove your previous features.
# =========================

import streamlit as st
import os
from dotenv import load_dotenv

# -------------------------
# Load ENV
# -------------------------
load_dotenv()

# IMPORTANT:
# Keep project name same as before
os.environ["LANGCHAIN_PROJECT"] = "Smart Chatbot"

# Optional but recommended in .env:
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=your_key

# -------------------------
# Imports
# -------------------------
from langsmith import uuid7
import backend

chatbot = backend.chatbot
connection = backend.connection

from langchain_core.messages import HumanMessage, AIMessage

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(
    page_title="Chat History Sidebar",
    layout="wide"
)

# ==========================================================
# SESSION STATE INIT
# ==========================================================

# -------------------------
# Load old thread IDs from SQLite checkpoints
# -------------------------
if "past_threads" not in st.session_state:
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
        threads = [row[0] for row in cursor.fetchall()]
        st.session_state["past_threads"] = threads
    except Exception:
        st.session_state["past_threads"] = []

# -------------------------
# Current thread selection
# -------------------------
if "thread_id" not in st.session_state:

    if st.session_state["past_threads"]:
        # Use last thread if exists
        st.session_state["thread_id"] = st.session_state["past_threads"][-1]
    else:
        # Create first thread
        new_id = str(uuid7())
        st.session_state["thread_id"] = new_id
        st.session_state["past_threads"].append(new_id)

# -------------------------
# Load messages from LangGraph state
# -------------------------
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if not st.session_state["message_history"]:

    config = {
        "configurable": {
            "thread_id": st.session_state["thread_id"]
        }
    }

    try:
        state = chatbot.get_state(config)

        if state.values and "messages" in state.values:
            history = []

            for msg in state.values["messages"]:
                role = "user" if isinstance(msg, HumanMessage) else "assistant"

                history.append({
                    "role": role,
                    "content": msg.content
                })

            st.session_state["message_history"] = history

        else:
            st.session_state["message_history"] = []

    except Exception:
        st.session_state["message_history"] = []

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("Settings")

    # -----------------------------------
    # New Chat
    # -----------------------------------
    if st.button("➕ New Chat"):

        new_id = str(uuid7())

        st.session_state["thread_id"] = new_id
        st.session_state["message_history"] = []

        if new_id not in st.session_state["past_threads"]:
            st.session_state["past_threads"].append(new_id)

        st.rerun()

    # -----------------------------------
    # Chat History Buttons
    # -----------------------------------
    st.subheader("Chat History")

    for tid in st.session_state["past_threads"]:

        label = f"🧵 {tid}"

        if tid == st.session_state["thread_id"]:
            label = f"🔵 {tid} (Current)"

        if st.button(label, key=f"btn_{tid}"):

            st.session_state["thread_id"] = tid

            config = {
                "configurable": {
                    "thread_id": tid
                }
            }

            state = chatbot.get_state(config)

            if state.values and "messages" in state.values:

                history = []

                for msg in state.values["messages"]:
                    role = "user" if isinstance(msg, HumanMessage) else "assistant"

                    history.append({
                        "role": role,
                        "content": msg.content
                    })

                st.session_state["message_history"] = history

            else:
                st.session_state["message_history"] = []

            st.rerun()

    st.divider()

    # -----------------------------------
    # Manual Thread ID
    # -----------------------------------
    manual_tid = st.text_input(
        "Manual Thread ID",
        value=st.session_state["thread_id"]
    )

    if manual_tid != st.session_state["thread_id"]:

        st.session_state["thread_id"] = manual_tid

        if manual_tid not in st.session_state["past_threads"]:
            st.session_state["past_threads"].append(manual_tid)

        st.rerun()

    # -----------------------------------
    # Clear UI Only
    # -----------------------------------
    if st.button("🧹 Clear Current UI"):

        st.session_state["message_history"] = []
        st.rerun()

# ==========================================================
# MAIN CHAT UI
# ==========================================================

st.title("💬 Chatbot with History")

# -------------------------
# Show Previous Messages
# -------------------------
for msg in st.session_state["message_history"]:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================================
# USER INPUT
# ==========================================================

user_input = st.chat_input("Type here :")

if user_input:

    # -----------------------------------
    # Show User Message
    # -----------------------------------
    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # ======================================================
    # IMPORTANT CHANGE STARTS HERE
    # ======================================================
    # We keep LangGraph thread_id for memory
    # AND add LangSmith session metadata for Threads UI
    # ======================================================

    current_tid = st.session_state["thread_id"]

    CONFIG = {
        "configurable": {
            "thread_id": current_tid   # LangGraph memory thread
        },

        # LangSmith better grouping
        "metadata": {
            "ls_session_id": current_tid,
            "thread_id": current_tid,
            "conversation_id": current_tid
        },

        "run_name": "Chat Session",

        "tags": [
            "streamlit",
            "langgraph",
            "chatbot"
        ]
    }

    # ======================================================
    # ASSISTANT RESPONSE
    # ======================================================

    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        try:
            # Keep your original stream mode
            # NOT removed
            for event in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="values"
            ):

                if "messages" in event:

                    last_message = event["messages"][-1]

                    if isinstance(last_message, AIMessage):
                        if last_message.tool_calls:
                            full_response = "🔧 *Calling tools...*"
                        else:
                            full_response = last_message.content
                        placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"Error: {str(e)}"
            placeholder.markdown(full_response)

        # Save assistant reply
        if full_response:

            st.session_state["message_history"].append({
                "role": "assistant",
                "content": full_response
            })