import streamlit as st
import requests
import io

st.title("FastAPI Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, bytes):
            st.audio(io.BytesIO(content), format='audio/wav')  # Wrap bytes in BytesIO
        else:
            st.markdown(content)

# Chat input
prompt = st.chat_input("Ask Something")
response_type = st.selectbox("Choose AI reply type", ["Text", "Audio"])

if prompt:
    # Show user message immediately
    st.chat_message("user").text(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Step 1: Generate text
    text_response = requests.get("http://localhost:8000/generate/text", params={"prompt": prompt})
    text_response.raise_for_status()
    ai_text = text_response.text

    # Step 2: Generate AI  audio  reply
    if response_type == "Text":
        ai_reply = ai_text
    else:
        audio_response = requests.get("http://localhost:8000/generate/audio", params={"prompt": ai_text})
        audio_response.raise_for_status()
        ai_reply = audio_response.content

    # Show assistant message
    with st.chat_message("assistant"):
        if response_type == "Text":
            st.markdown(ai_text)
        else:
            st.markdown(ai_text)
            st.audio(io.BytesIO(ai_reply), format='audio/wav')  # Wrap bytes in BytesIO

    # Save assistant message in session state
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
