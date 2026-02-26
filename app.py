import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader


st.title('Faculty Lesson Assistant')
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader('Upload a lesson plan')

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in reader.pages])

    specific_prompt = st.text_area(
        "Specific Instruction",
        value="Actúa como un experto en diseño instruccional y pedagogía universitaria. Analiza el documento adjunto, el cual corresponde al programa oficial de un curso de la Universidad Técnica Nacional. Tu tarea es examinar los propósitos generales y específicos del curso e identificar cómo se alinean con las habilidades (cognitivas, técnicas y prácticas) y las actitudes (valores, competencias blandas y profesionales) que se exigen de forma explícita o implícita en el documento. Presenta tu análisis en una tabla estructurada que vincule: 1) Propósito del curso, 2) Habilidades asociadas, 3) Actitudes requeridas. Finalmente, incluye un breve párrafo identificando si existe alguna brecha de alineación curricular que el docente deba subsanar durante el desarrollo de las clases."
    )
    if st.button("Process Instruction"):
        with st.spinner("Processing..."):
            model = genai.GenerativeModel('gemini-2.5-flash')
            res = model.generate_content(f"{specific_prompt}\n\nContext: {text}")
            st.session_state.messages.append({"role": "user", "content": specific_prompt})
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            st.rerun()
    
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
