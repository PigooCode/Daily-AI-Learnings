import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
from uuid import uuid4

# Utility functions

def generate_thread_id():
    return str(uuid4())

def reset_chat():
    st.session_state['message_history'] = []
    st.session_state['thread_id'] = generate_thread_id()

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_thread(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id': thread_id}}).values['messages']

# Initialize message history in session state

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])


# Sidebar UI

st.sidebar.title("Langgraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()
    add_thread(st.session_state['thread_id'])

st.sidebar.header('My conversations')

for thread_id in st.session_state['chat_threads'][::-1]:  # Show most recent threads first
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        msg = load_thread(thread_id)

        tmp_msg = []

        for message in msg:
            if isinstance(message, HumanMessage):
                tmp_msg.append({'role': 'user', 'content': message.content})
            else:
                tmp_msg.append({'role': 'assistant', 'content': message.content})
        
        st.session_state['message_history'] = tmp_msg

# Main UI

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    config = {'configurable':{'thread_id': st.session_state['thread_id']}}

    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config=config,
            stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})