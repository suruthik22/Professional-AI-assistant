from langchain_text_splitters import RecursiveCharacterTextSplitter
from preprocess import combine_data

def chunk_documents():
    documents=combine_data()

    splitter=RecursiveCharacterTextSplitter(chunk_size=1200,chunk_overlap=350)

    chunks=splitter.split_documents(documents)

    return chunks

if __name__=="__main__":
    chunks=chunk_documents()
    print(f"Total chunks created:{len(chunks)}")
