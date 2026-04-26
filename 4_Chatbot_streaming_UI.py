import streamlit as st

# Set page config
st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖", layout="centered")

# Custom CSS for full black UI and light (white) input box
st.markdown("""
    <style>
    /* Full Black Background */
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    /* Header/Top Bar */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    /* Light Input Box with Circular Ends */
    .stChatInputContainer {
        background-color: transparent !important;
        padding-bottom: 30px !important;
    }
    
    .stChatInput textarea {
        border-radius: 30px !important;
        background-color: #f0f2f6 !important; /* Light Gray/White */
        color: #000000 !important;           /* Black text for light box */
        border: 2px solid #ffffff !important;
        padding-left: 20px !important;
        font-size: 16px !important;
    }

    /* Send button styling to make it visible on light box */
    .stChatInput button {
        color: #000000 !important;
    }

    /* Message bubbles */
    [data-testid="stChatMessage"] {
        background-color: #1a1a1a !important; /* Slightly lighter than black for depth */
        border-radius: 20px !important;
        border: 1px solid #333 !important;
    }

    /* All text white except for input box */
    h1, h2, h3, p, span, div, label {
        color: #ffffff !important;
    }
    
    /* Ensure the input box text stays black */
    .stChatInput textarea {
        -webkit-text-fill-color: #000000 !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #000000;
    }
    ::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI Assistant")

# Show a loading message while importing backend
with st.spinner("Preparing Intelligence..."):
    try:
        from chatbot_backend import chatbot
        from langchain_core.messages import HumanMessage, AIMessage
    except Exception as e:
        st.error(f"Initialization Error: {e}")
        st.stop()

st.markdown("---")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerender
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type your message here..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Stream the chatbot response
                config = {"configurable": {"thread_id": "user_session_1"}}
                
                # Create a placeholder for the response
                response_placeholder = st.empty()
                full_response = ""
                
                # Use stream_mode="values" to get the latest state
                for event in chatbot.stream({"messages": [HumanMessage(content=prompt)]}, config=config, stream_mode="values"):
                    if "messages" in event:
                        last_message = event["messages"][-1]
                        if isinstance(last_message, AIMessage):
                            full_response = last_message.content
                            response_placeholder.markdown(full_response)
                
                # Save to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Model Error: {e}")
