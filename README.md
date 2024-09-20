# AI Cover Letter Generator

This repository contains the code for the **AI Cover Letter Generator**, a tool designed to help users generate personalized cover letters based on their resume and job description inputs. The project utilizes **Mistral Nemo LLM**, the **Streamlit** framework, and **Hugging Face Inference API** to provide an efficient and intelligent solution for creating cover letters.

## Features
- **Personalized Cover Letters:** Generate tailored cover letters by providing resume details and job descriptions.
- **AI-Powered (Mistral Nemo LLM):** Leverages the Mistral Nemo large language model (LLM) for intelligent, context-aware generation of unique cover letters.
- **Hugging Face Integration:** Uses the Hugging Face Inference API to connect with the LLM, ensuring fast and accurate results.
- **User-Friendly Interface (Streamlit):** Built with Streamlit, providing a clean and interactive interface for inputting information and generating cover letters.
- **Fast & Efficient:** Generates results in seconds, saving you time in your job application process.
- **File Support (DOCX & PDF):** Utilizes `docx2txt` for extracting text from DOCX files and `pypdf` for handling PDF files, allowing seamless input from a variety of file formats.

## Deployed Demo
The cover letter generator app is deployed in one of my Hugging Face Spaces and can be accessed through this link:  
[AI Cover Letter Generator - Hugging Face](https://huggingface.co/spaces/omar-arif/cover-letter-generator)

![Deployed App Screenshot](cover_letter_genrator.png)

## How to Use

1. Clone the repository:
    ```bash
    git clone https://github.com/omar-arif/ai-cover-letter-generator.git
    ```

2. Navigate into the project directory:
    ```bash
    cd ai-cover-letter-generator
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your Hugging Face Token:
    - Create an account on [Hugging Face](https://huggingface.co/).
    - Go to your [Hugging Face settings](https://huggingface.co/settings/tokens) and create an API token.
    - Set the `HF_TOKEN` environment variable to the token value:
      ```bash
      export HF_TOKEN=your_huggingface_token
      ```

5. Run the app:
    ```bash
    streamlit run app.py
    ```

## Requirements
- Python 3.7+
- Required packages are listed in `requirements.txt`.
- Hugging Face API token.

## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](https://github.com/omar-arif/ai-cover-letter-generator/blob/main/LICENSE) file for more details.

