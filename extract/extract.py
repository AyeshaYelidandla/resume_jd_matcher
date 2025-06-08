import fitz
import re

def extract_text_from_pdf(pdf_path_or_file):
    text = ""
    try:
        with fitz.open(stream=pdf_path_or_file.read(), filetype="pdf") if not isinstance(pdf_path_or_file, str) else fitz.open(pdf_path_or_file) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        print("An error occurred during the extraction from pdf file:", e)
        return ""

def extract_jd_text(jd_path):
    with open(jd_path, 'r', encoding='utf-8') as f:
        return f.read()

def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()