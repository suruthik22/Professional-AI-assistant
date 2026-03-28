from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

github_token=os.getenv("GITHUB_TOKEN")
openai_key=os.getenv("OPENAI_API_KEY")

# -----------------------------
# LOAD PIPELINE
# -----------------------------
def load_pipeline():
    embeddings = OpenAIEmbeddings()

    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    return db, llm


# -----------------------------
# INTENT DETECTION
# -----------------------------
def detect_intent(query):
    q = query.lower()

    if "tell me about yourself" in q or "introduce yourself" in q or "tell about you" in q:
        return "intro"
    
    elif any(word in q for word in ["project", "built", "portfolio", "Projects"]):
        return "project"
    
    elif any(word in q for word in ["strength", "weakness", "challenge", "difficult", "problem"]):
        return "behavioral"
    
    else:
        return "general"


# -----------------------------
# RESPONSE GENERATORS
# -----------------------------
def generate_intro(context, llm):
    prompt = f"""
You are Suruthi speaking in a real interview. You are an experienced analyst. Do not hallucinate. Answer only on the context given. prioritise my CV and then my Github Projects

Give strong confident answers in a human natural tone but professionally to the recruiter asking questions.

Start with your background, explain your skills, then talk about your experience giving short relevant examples from CV and linkedin along with business impact.
Explain your abilities, skills including proficiency in technical tools. Also state your recent projects from github, what business value they create and how you are trying to learn new techniques and concepts. finally end with your expectations in new role and your career path
It should be like professional storytelling.
Answer based only on context. Do not repeat any projects. Give more priority to CV data.

Answer based only on context. Answer should be Minimum of 12 lines

Context:
{context}
"""
    return llm.invoke(prompt).content


def generate_behavioral(query, context, llm):
    prompt = f"""
You are Suruthi answering a behavioral interview question to the recruiter.
The answer should be like smooth story telling in a  natural human tone. Do not explicitly state but 
follow a STAR technique to answer the question. Be specific and professional and base it only on the context given.
Answer based only on context . do not hallucinate. Prioritise  CV 
Do not repeat any project
Question:
{query}

Context:
{context}
"""
    return llm.invoke(prompt).content


def generate_best_project(context, llm):
    prompt = f"""
You are Suruthi explaining your projects like in an interview to a recruiter.

Speak like you are explaining to a recruiter. The response should be like smooth story telling in a natural human but professional tone

First give a brief summary of your previous experience, areas of expertise and project experiences in one or 2 lines. Then dive into details.

Based on the key words from the query, match and list 2 to 3 most relevent projects, prioritising my Github projects in the first and then my CV

Structure the answer in STARR format but do not state explicitly. Explain what the business problem/situation was, What needed to be done and what was my contribution, the reasoning behind it, the tools used and the clear business impact/insights/results like a storytelling.
Do not just list 
Do not repeat any projects or experience. 

If asked explicitly on experience, prioritise CV, linkedin and then Github projects. If asked about projects, start with a brief summary of your experience in various organisations and then explain about github projects

Context:
{context}
"""

    return llm.invoke(prompt).content


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def ask_bot(query, top_k=10):

    if not os.path.exists("chroma_db"):
        from src.vector_store import create_vector_store
        create_vector_store()

    db, llm = load_pipeline()

    intent = detect_intent(query)

    # -----------------------------
    # BASE RETRIEVAL
    # -----------------------------
    docs = db.similarity_search(query, k=top_k)

    # -----------------------------
    # FORCE CONTACT RETRIEVAL
    # -----------------------------
    contact_docs = db.similarity_search("email linkedin contact", k=2)

    # -----------------------------
    # BOOST PROJECT RETRIEVAL
    # -----------------------------
    if intent == "project":
        project_docs = db.similarity_search(
            "projects machine learning analytics pipeline dashboard",
            k=15
        )
        docs.extend(project_docs)

    # -----------------------------
    # REMOVE DUPLICATES SAFELY
    # -----------------------------
    seen = set()
    unique_docs = []

    for doc in docs + contact_docs:
        if doc.page_content not in seen:
            unique_docs.append(doc)
            seen.add(doc.page_content)

    docs = unique_docs

    # -----------------------------
    # BUILD CONTEXT (CLEAN FORMAT)
    # -----------------------------
    context = "\n\n".join([
        f"""
SOURCE: {doc.metadata.get('source')}
PROJECT: {doc.metadata.get('project','N/A')}

{doc.page_content}
"""
        for doc in docs
    ])

    # -----------------------------
    # GENERATE SOURCES
    # -----------------------------
    sources = list(set([
        f"{doc.metadata.get('source')} - {doc.metadata.get('project','')}"
        for doc in docs
    ]))

    # -----------------------------
    # ROUTING
    # -----------------------------
    if intent == "intro":
        answer = generate_intro(context, llm)

    elif intent == "project":
        answer = generate_best_project(context, llm)

    elif intent == "behavioral":
        answer = generate_behavioral(query, context, llm)

    else:
        # DEFAULT RAG
        prompt = f"""
You are Suruthi answering in a real interview to the queries raised by a recruiter.
Sound like a human and not AI. The answers should be like a smooth storytelling but professional and based only on the context

Based on the question start with a confident direct summary of 1 to 3 lines and then dive deeper by supporting with real example of project or experience based on my Github and CV, then clearly explain what you did in the project or experience, and conclude with business impact or results

Integrate your answers with the tools , skills used in the situation. 
The response should be conversational like speaking but should be professional

Prioritise my CV and then GitHub + real projects .If tools are mentioned → show HOW you used them, not just name them
Think like a strong candidate, not a summary bot
Answer ONLY from context

Always use exact email and LinkedIn from context
If any personal questions are asked and if any questions are asked to which you are not able to respond from the given context,
give a short relevant summary and politely ask them to reach out to you on your linkedin profile or email by explicitly giving the relevant profile link and email address

Context:
{context}

Question:
{query}

Answer:
"""
        answer = llm.invoke(prompt).content

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------
    return answer + "\n\nSources:\n" + "\n".join(sources)