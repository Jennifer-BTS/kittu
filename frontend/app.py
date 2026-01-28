import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 KITTU")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to backend
    response = requests.post(
        BACKEND_URL,
        json={"message": user_input}
    )

    if response.status_code == 200:
        bot_reply = response.json().get("reply", "⚠️ No reply field.")
    else:
        bot_reply = "⚠️ Backend error."

    # Add bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
