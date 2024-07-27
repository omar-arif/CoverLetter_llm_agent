import streamlit as st
from pypdf import PdfReader
import docx2txt

st.write("Hello! Welcome to my new app")
uploaded_file = st.file_uploader('upload your resume (pdf or docx file)', type=["pdf","docx"])
if uploaded_file is not None:
    suffix = uploaded_file.name.split(".")[-1]
    cv_text = ""

    match suffix:
        case "pdf":
            reader = PdfReader(uploaded_file) 
            for page in reader.pages:
                cv_text += page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False, layout_mode_scale_weight=1.0)
            st.write(cv_text)
        case "docx":
            cv_text = docx2txt.process(uploaded_file)
            st.write(cv_text)