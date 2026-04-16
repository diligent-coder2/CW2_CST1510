import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not found in environment variables.")
    st.info("Please set the GROQ_API_KEY in your .env file and restart the app.")
    st.info("You can obtain an API key from https://console.groq.com/keys and add it to your .env file as follows:")
    st.code('GROQ_API_KEY=your_api_key_here', language='bash')
    st.stop()
client = Groq(api_key=api_key)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to Home page"):
        st.switch_page("Home.py")
    st.stop()

st.success(f"Hello, **{st.session_state.user['login_username']}**! You are logged in.")
st.title('Chat with groq')

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

with st.sidebar:
    st.header('Navigation')
    if st.button('Clear chat(s)'):
        sleep(2)
        st.session_state.messages = []
    st.divider()
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.user = {}
        st.session_state.messages = []
        st.info("You have been logged out.")
        sleep(2)
        st.switch_page("Home.py")

for message in st.session_state.messages:
    st.chat_message(message['role']).write(message['content'])

prompt = st.chat_input('Enter your message:')

if prompt:
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    st.chat_message('user').write(prompt)

    completion = client.chat.completions.create(
        model= 'openai/gpt-oss-120b',
        messages= st.session_state.messages
    )

    reply = completion.choices[0].message.content
    st.session_state.messages.append({'role': 'assistant', 'content': reply})
    st.chat_message('assistant').write(reply)
