import os
from pypdf import PdfReader
from docx import Document

def extract_text_from_pdf(file_path):
    reader=PdfReader(file_path)
    return " ".join([page.extract_text() or "" for page in reader.pages])

def extract_text_from_docx(file_path):
    doc=Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path,"r",encoding="utf-8") as f:
        return f.read()
    
def process_cv():
    folder="data/raw"
    cv_text=""

    for file in os.listdir(folder):
        file_path=os.path.join(folder,file)

        if file.endswith(".pdf"):
            cv_text += extract_text_from_pdf(file_path)
        
        elif file.endswith(".docx"):
            cv_text+=extract_text_from_docx(file_path)

        elif file.endswith(".txt"):
            cv_text+=extract_text_from_txt(file_path)

    with open("data/processed/cv_cleaned.txt","w",encoding="utf-8") as f:
        f.write(cv_text)

if __name__=="__main__":
    process_cv()