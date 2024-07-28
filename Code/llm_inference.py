import streamlit as st
from pypdf import PdfReader
import docx2txt

def ingest_document(stream):
    '''
        A function that takes a BytesIO in-memory stream, decodes the content into a string
        then returns it.
        the stream is either from a pdf or a docx file.
    '''

    # get the uploaded document's extension
    suffix = stream.name.split(".")[-1]
    content_text = ""

    match suffix:
        # extract text if pdf file with pypdf
        case "pdf":
            reader = PdfReader(stream) 
            for page in reader.pages:
                content_text += page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False, layout_mode_scale_weight=1.0)
        
        # extract text if docx file with docx2txt
        case "docx":
            content_text = docx2txt.process(stream)
    
    return content_text



st.title("Welcome to the AI Cover Letter Generator :sparkles:")

# create a form in order to only run the code below if a submit button is pressed
with st.form("my_form"):
    # get resume and cover letter uploaded
    uploaded_resume = st.file_uploader('Upload your resume :point_down:', type=["pdf","docx"])
    uploaded_job_description = st.file_uploader('Upload the description of the job you\'re wishing to apply for :point_down:', type=["pdf","docx"])
    resume_text = ""

    # ingest uploaded documents
    if uploaded_resume is not None:
        resume_text += ingest_document(uploaded_resume)
    if uploaded_job_description is not None:
        resume_text += ingest_document(uploaded_job_description)

    # if the submit button is pressed execute code inside the if statement
    submitted = st.form_submit_button("Generate Cover Letter :printer:")
    if submitted:
        # display errors if one of the files required is not uploaded
        if uploaded_resume is None:
            st.error("Your Resume is missing! :rotating_light:")
        elif uploaded_job_description is None:
            st.error("The job description is missing! :rotating_light:")
        else:
            st.write(resume_text)


    