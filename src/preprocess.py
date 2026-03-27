from langchain_core.documents import Document
import json


def combine_data():
    documents=[]

    #CV 
    with open("data/processed/cv_cleaned.txt",encoding="utf-8") as f:
            documents.append(
                 Document(
                       page_content=f.read(),
                       metadata={"source":"cv"}
                       )
            )
    
    #Linkedin
    with open("data/processed/linkedin_cleaned.txt",encoding="utf-8") as f:
            documents.append(
                 Document(
                       page_content=f.read(),
                       metadata={"source":"linkedin"}
                       )
            )
    
    #github data
    with open("data/raw/github.json") as f:
        github=json.load(f)
        for repo in github:
            documents.append(
                  Document(
                        page_content=f"""
                        Project Name:{repo['Project name']}
                        Project Description:{repo['Project description']}
                        Project Details:{repo['Project content']}
                        Keywords: projects, experience, data, project, data science, machine learning, dashboard, ETL, NHS, analytics, python, PowerBI, SQL, excel, data
                        """,
                        metadata={"source":"github",
                                  "project":repo["Project name"]
                                  }
                                  )
            )
    
    return documents