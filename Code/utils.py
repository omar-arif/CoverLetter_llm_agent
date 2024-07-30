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
    
    def __init__(self, resume, job_desc, model_id="mistralai/Mistral-Nemo-Instruct-2407", language="English", word_count=350):
        # model_id is the id of the huggingface repository of the model
        self.model_id = model_id
        self.language = language
        self.word_count = word_count

        # prompt messages structure : system role is used in order to supervise the model's behaviour, user role is used to ask for the generation of the cover letter
        match self.language:
            case "English":
                self.messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that specializes in helping candidates to write and format their cover letters. Your will use the language they use to speak to you",
            },
            {
                "role": "user",
                "content": "whitout any headers, write in less than " + str(self.word_count) + "words a simple but professional way, a cover letter based on my resume and the description of the job I am applying for below  :\n Resume: " + resume + "\n Job description: " + job_desc,
            },
        ]
            case "Français":
                self.messages = [
            {
                "role": "system",
                "content": "Vous êtes un assistant utile qui se spécialise dans l'aide aux candidats pour rédiger et mettre en forme leurs lettres de motivation.",
            },
            {
                "role": "user",
                "content": "Sans aucune entête, écrivez en moins de " + str(self.word_count*0.75) + "mots et de manière simple mais professionnelle une lettre de motivation basée sur mon CV et l'offre d'emploi du poste auquel je postule ci-dessous  :\n CV: " + resume + "\n offre d'emploi: " + job_desc,
            },
        ]
                
        # get the token from HF_TOKEN environement variable
        hf_token = os.environ.get('HF_TOKEN')
        self.api_token = hf_token
        
        self.inference_client = InferenceClient(model=model_id, token=hf_token, timeout=120)
    
    def generate_letter(self):
        # convert word count to number of tokens and add a safety margin
        token_number = int(self.word_count//0.75) + 100
        # call the inference api and generate answers
        data = self.inference_client.chat_completion(self.messages, max_tokens=token_number)
        return data.choices[0].message.content