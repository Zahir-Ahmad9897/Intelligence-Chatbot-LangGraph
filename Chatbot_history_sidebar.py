import streamlit as st
import uuid
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage

# Page config MUST be the first streamlit command
st.set_page_config(page_title="Chat History Sidebar", layout="wide")

# Initialize session state
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
if 'past_threads' not in st.session_state:
    st.session_state['past_threads'] = []
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = "thread_1"
    st.session_state['past_threads'].append("thread_1")

# Sidebar for history / settings
with st.sidebar:
    st.title("Settings")
    
    if st.button("➕ New Chat"):
        import uuid
        new_id = str(uuid.uuid4())[:8]
        st.session_state['thread_id'] = new_id
        st.session_state['message_history'] = []
        if new_id not in st.session_state['past_threads']:
            st.session_state['past_threads'].append(new_id)
        st.rerun()

    st.subheader("Chat History")
    for tid in st.session_state['past_threads']:
        # Highlight current thread
        label = f"🧵 {tid}"
        if tid == st.session_state['thread_id']:
            label = f"🔵 {tid} (Current)"
        
        if st.button(label, key=f"btn_{tid}"):
            st.session_state['thread_id'] = tid
            # Fetch history from LangGraph checkpointer
            config = {'configurable': {'thread_id': tid}}
            state = chatbot.get_state(config)
            if state.values and 'messages' in state.values:
                # Convert LangGraph messages back to UI format
                history = []
                for msg in state.values['messages']:
                    role = "user" if isinstance(msg, HumanMessage) else "assistant"
                    history.append({"role": role, "content": msg.content})
                st.session_state['message_history'] = history
            else:
                st.session_state['message_history'] = []
            st.rerun()

    st.divider()
    thread_id = st.text_input("Manual Thread ID", value=st.session_state['thread_id'])
    if thread_id != st.session_state['thread_id']:
        st.session_state['thread_id'] = thread_id
        if thread_id not in st.session_state['past_threads']:
            st.session_state['past_threads'].append(thread_id)
        st.rerun()

    if st.button("🧹 Clear Current UI"):
        st.session_state['message_history'] = []
        st.rerun()

st.title("💬 Chatbot with History")

# Display conversation history 
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# User input
user_input = st.chat_input('Type here :')

if user_input:
    # Add user message to history and display
    st.session_state['message_history'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
    
    # Assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Using stream_mode="values" to get the latest state which includes the AIMessage
        for event in chatbot.stream({"messages": [HumanMessage(content=user_input)]}, config=CONFIG, stream_mode="values"):
            if "messages" in event:
                last_message = event["messages"][-1]
                if isinstance(last_message, AIMessage):
                    full_response = last_message.content
                    response_placeholder.markdown(full_response)
        
        # Save assistant message to history
        if full_response:
            st.session_state['message_history'].append({"role": "assistant", "content": full_response})
        
               