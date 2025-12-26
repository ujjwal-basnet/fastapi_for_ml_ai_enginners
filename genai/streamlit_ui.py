import streamlit as st
import requests 

st.title("FastAPI chatbot")

#Checks if messages exists in the session state, If not, it initializes st.session_state.messages
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages: #Loops over all messages stored in st.session_state.messages
    with st.chat_message(message["role"]):  # st.chat_message(message["role"]) creates a chat bubble for each message
        st.markdown(message["content"]) # display message insided chat bubble

prompt = st.chat_input("Ask Someting") #  creates chat input box


if prompt: # Checks if the user entered something 
    st.session_state.messages.append({"role" : "user", "content" : prompt}) ## it just save msg immediatly in session state , but if you end code here and run , you you type 
    # hellow , it wont show , and types hi -> it will show previoud msg , because , first ui render in loop and then msg 

    with st.chat_message("user"): ##Create a chat bubble for the current user message 
        st.text(prompt) # display msg immediatly

    response= requests.get(f"http://localhost:8000/generate/text", 
                    params= {"prompt" : prompt})
    response.raise_for_status()

    with st.chat_message("assistant"): ## asistant measn just yellow chat bupple like dp 
        st.markdown(response.text)



################## please run main.py first and then , it use response form main.py ######## 
  ### to run 
  # command : streamlit run ./genai/streamlit_ui.py 
  # on  terminal 