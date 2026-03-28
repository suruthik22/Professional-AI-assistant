from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.chunking import chunk_documents
from dotenv import load_dotenv
import os

load_dotenv()

github_token=os.getenv("GITHUB_TOKEN")
openai_key=os.getenv("OPENAI_API_KEY")

def create_vector_store():
    chunks=chunk_documents()

    embeddings=OpenAIEmbeddings()

    db=Chroma(embedding_function=embeddings,
              persist_directory="chroma_db")
    
    db.add_documents(chunks)
    
    print(f"\nVector embedding created...\n")

if __name__=="__main__":
    create_vector_store()
    
