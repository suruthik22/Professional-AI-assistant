# Suruthi's Professional AI assistant
This is a Personal chatbot that can answer questions on my professional background, experience and projects. It stemmed from the idea that "What if recruiters could have a real conversation with my experience anytime, instantly? without the standard hardcode CV"

# APP LINK
https://ask-suruthi.streamlit.app/ 

# Introduction
This is an AI powered digital twin chatbot built so that recruiters or any person can have a natural, conversation on my professional profile like my experience, technical skills, projects, work eligibility, availability or career goals without a formal call. It would respond the way I would backed by real examples from my CV, Linkedin and GitHub.

# Brief
This project is an AI powered chatbot designed using an end-to-end Retrieva Augmented Generation (RAG) pipeline. It integrates data from multiple sources, including a CV (PDF/text), LinkedIn profile (CSV archive export) and GitHub repositories through API. The data is ingested, cleaned and structured into a unified format using LangChain document schemas. The processed content is then chunked and transformed into vector embeddings using OpenAI models, which are stored in a ChromaDB vector database. A RAG pipeline is implemented to enable context aware retrieval and response generation using an OpenAI LLM. The system is designed to simulate real-time, interview-style interactions with human-like responses. The application is deployed as an interactive web interface on Streamlit Cloud.

# Tech stack
1. IDE - VSCode
2. Language / Tools - Python
3. Front End / deployment - Streamlit 
4. Embeddings and LLM - Open AI
5. Vector Store - ChromaDB
6. Documentation/ Orchestration - langchain

# Technical concepts
1. Retrieval Augmented Generation (RAG) - Documentation, Chunking, Embedding in Vector store, Retrieval and Generation
2. FAST API
4. LLM
5. Deployment
6. Machine Learning, Prompt Engineering
7. ETL pipeline

# Example questions to try
1. Tell me about yourself
2. What experience do you have with data pipelines?
3. Walk me through your most impactful project
4. What tools are you proficient in?

# Applications
The concept and approach can be used contract management, HR people information management, SOP understanding, Quality Management Systems, etc

# Architecture 

<img width="398" height="713" alt="image" src="https://github.com/user-attachments/assets/4fa8577c-e810-4806-a24b-24ae7fbeb911" />


┌─────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                         │
│     CV (PDF/TEXT)    LinkedIn (CSV)    GitHub (API)        │
└──────────────┬──────────────┬──────────────┬───────────────┘
               │              │              │
               └──────────────▼──────────────┘
                    LangChain Document Loader
                              │
                    ┌─────────▼─────────┐
                    │   Text Chunking   │
                    │  + OpenAI Embed   │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  ChromaDB Vector  │
                    │      Store        │
                    └─────────┬─────────┘
                              │
               ┌──────────────▼──────────────┐
               │        RAG Pipeline         │
               │  Retrieval → Prompt Route   │
               │  → GPT-4o-mini → Response   │
               └──────────────┬──────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Streamlit Cloud  │
                    │    (Public UI)    │
                    └───────────────────┘
