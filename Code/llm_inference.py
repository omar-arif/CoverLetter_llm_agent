import streamlit as st
from pypdf import PdfReader
import docx2txt

def ingest_document(stream):
    '''
        A function that takes a BytesIO in-memory stream, decodes the content into a string
        then returns it.
        the stream is either from a pdf or a docx file.
    '''

    suffix = stream.name.split(".")[-1]
    content_text = ""

    match suffix:
        case "pdf":
            reader = PdfReader(stream) 
            for page in reader.pages:
                content_text += page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False, layout_mode_scale_weight=1.0)
        case "docx":
            content_text = docx2txt.process(stream)
    
    return content_text



st.write("Hello! Welcome to my new app")
uploaded_file = st.file_uploader('upload your resume (pdf or docx file)', type=["pdf","docx"])
if uploaded_file is not None:
    resume_text = ingest_document(uploaded_file)
    st.write(resume_text)
    