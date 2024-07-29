from pypdf import PdfReader
import docx2txt
from huggingface_hub import InferenceClient
import os


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
            for i, page in enumerate(reader.pages):
                # don't take over 2 pages of the job description (could be too many tokens)
                if i > 3:
                    break
                content_text += page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False, layout_mode_scale_weight=1.0)
        
        # extract text if docx file with docx2txt
        case "docx":
            content_text = docx2txt.process(stream)
    
    return content_text

class CoverLetterMaker():
    
    def __init__(self, resume, job_desc, model_id="microsoft/Phi-3-mini-4k-instruct"):
        self.model_id = model_id
        
        self.user_content =  "Write in a simple but professional way a cover letter based on my resume and the description of the job i am applying for below  :\n Resume: " + resume + "\n Job description: " + job_desc
        
        hf_token = os.environ.get('HF_TOKEN')
        self.api_token = hf_token
        
        self.inference_client = InferenceClient(model=model_id, token=hf_token, timeout=120)
        
        self.messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that specializes in helping candidates to write and format their cover letters. Your are fluent in both french and english",
    },
    {
        "role": "user",
        "content": self.user_content,
    },
]
    
    def generate_letter(self, max_tokens=500):
        data = self.inference_client.chat_completion(self.messages, max_tokens=max_tokens)
        return data.choices[0].message.content