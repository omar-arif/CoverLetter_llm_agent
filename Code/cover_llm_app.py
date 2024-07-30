import streamlit as st
import utils

st.title("Welcome to the AI Cover Letter Generator :sparkles:")

# get resume uploaded
with st.container(border=True):
    
    uploaded_resume = st.file_uploader('Upload your resume :point_down:', 
                                       type=["pdf","docx"], 
                                       key="resume doc upload")


# get the job description either by uploading a pdf/docx file or by text
uploaded_job_description = None
filled_job_description = ""

with st.container(border=True):
    
    option = st.radio(
    "Job description format :briefcase:",
    ("pdf/docx", "Text"),)

    match option:
        case "pdf/docx":
            uploaded_job_description = st.file_uploader('Upload the description of the job you\'re wishing to apply for :point_down:', type=["pdf","docx"],key="job desc doc upload")

        case "Text":
            filled_job_description = st.text_area('Input the description of the job you\'re wishing to apply for :point_down:', max_chars=5000)


# get language and word count of the cover letter in a dedicated container
with st.container(border=True):
    
    language = st.radio(
    "Which language would you like to use? :scroll:",
    ("Français", "English"),)
    word_count = st.slider("How many long would you like your cover letter to be? (word count) :writing_hand:", 50, 500, 300)


# create a form in order to only run the code below if a submit button is pressed
with st.form("generator_form", border=False):

    resume_text = ""
    job_desc_text = ""

    # ingest uploaded documents
    if uploaded_resume is not None:
        resume_text += utils.ingest_document(uploaded_resume)

    if uploaded_job_description is not None:
        job_desc_text += utils.ingest_document(uploaded_job_description)
    
    elif len(filled_job_description) != 0:
        job_desc_text += filled_job_description

    # if the submit button is pressed execute code inside the if statement
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        submitted = st.form_submit_button("Generate Cover Letter :printer:")

    if submitted:
        # display errors if one of the files required is not uploaded
        if uploaded_resume is None:
            st.error("Your Resume is missing! :rotating_light:")

        elif uploaded_job_description is None and len(filled_job_description)==0:
            st.error("The job description is missing! :rotating_light:")

        else:
            # HF_TOKEN environement variable should be set to the huggingface token of the user
            cover_maker = utils.CoverLetterMaker(resume=resume_text, job_desc=job_desc_text, language=language, word_count=word_count)
            st.write(cover_maker.generate_letter())


    