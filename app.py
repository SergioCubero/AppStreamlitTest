import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()

st.title('Faculty Lesson Assistant')
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader('Upload a lesson plan')

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in reader.pages])

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"]) 

    if prompt := st.chat_input("Ask about the lesson plan"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        model = genai.GenerativeModel('gemini-2.5-flash')
        res = model.generate_content(f"Use this lesson plan as context: {text}\n\nQuestion: {prompt}")

        st.session_state.messages.append({"role": "assistant", "content": res.text})
        with st.chat_message("assistant"):
            st.markdown(res.text)