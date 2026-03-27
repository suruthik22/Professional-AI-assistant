import streamlit as st 
from src.rag_pipeline import ask_bot 

st.set_page_config(page_title="Suruthi AI Assistant", 
                   page_icon="🤖", 
                   layout="centered") 
# -------------------------- 
# HEADER 
# -------------------------- 
st.markdown(""" 
            <style> /* Background */ 
            .stApp { 
            background: linear-gradient(135deg, #0f2027, #2c5364, #00c9a7); 
            color: white; 
            } 
            /* Title */ 
            h1 { text-align: center; 
            color: #ffffff; 
            font-size: 40px; 
            } 
            /* Input box */ 
            .stTextInput > div > div > input { 
            background-color: #ffffff; color: black;
             border-radius: 10px;
             padding: 10px; 
            } 
            /* Response box */ 
            .response-box {
             background-color: rgba(255,255,255,0.08);
             padding: 20px; 
            border-radius: 15px;
             margin-top: 20px;
             }
             /* Force ALL chat text to white */
            [data-testid="stChatMessageContent"] {
                color: white !important;
            }

            /* Make markdown text inside chat white */
            [data-testid="stMarkdownContainer"] p,
            [data-testid="stMarkdownContainer"] li,
            [data-testid="stMarkdownContainer"] span {
                color: white !important;
            }

            /* Fix headings inside responses (like Project titles) */
            [data-testid="stMarkdownContainer"] h1,
            [data-testid="stMarkdownContainer"] h2,
            [data-testid="stMarkdownContainer"] h3 {
                color: white !important;
            }
                  
            /* Sources box */ 
            .sources-box {
                background-color: rgba(0,0,0,0.4);
                padding: 15px;
                border-radius: 10px;
                margin-top: 15px;
                font-size: 14px;
                color: white !important;   /* ← IMPORTANT FIX */
            }

            /* Ensure links (if any) are visible */
            .sources-box a {
                color: #00c9a7 !important;
            }
             /* Button */ 
            .stButton button { 
            background-color: #00c9a7;
             color: white;
             border-radius: 10px; 
            padding: 10px 20px;
             border: none; 
            } 

            /* Spinner color fix */
            [data-testid="stSpinner"] svg {
                stroke: white !important;
            }

            /* Spinner text (Thinking...) */
            [data-testid="stSpinner"] {
                color: white !important;
            }
            </style> 
            <h1 style='text-align: center;'>🤖 Suruthi's AI Assistant</h1>
            <p style='text-align: center; color: white;'> Ask me anything about my professional experience, projects or skills </p>
            """, unsafe_allow_html=True) 
st.divider() 
# -------------------------- 
# CHAT HISTORY 
# --------------------------
if "messages" not in st.session_state: 
    st.session_state.messages = [] 
    
# Display chat 
for msg in st.session_state.messages: 
    with st.chat_message(msg["role"]): 
        st.markdown(msg["content"]) 

# -------------------------- 
# USER INPUT
# -------------------------- 
query = st.chat_input("Ask a question...") 
if query: 
    # Save user message 
    st.session_state.messages.append({"role": "user", "content": query}) 
    with st.chat_message("user"): 
        st.markdown(query) 
    
    # Generate response 
    with st.chat_message("assistant"): 
        with st.spinner("Thinking..."): 
            response = ask_bot(query) 
        
        # Split answer + sources 
        if "Sources:" in response: 
            answer, sources = response.split("Sources:") 
        else: answer, sources = response, "" 
        
        # Show answer 
        st.markdown(answer) 
        
        # Show sources separately 
        if sources.strip(): 
            st.markdown("### 📌 Sources") 
            st.markdown(f"<small>{sources}</small>", 
                        unsafe_allow_html=True) 
    
    # Save assistant response 
    st.session_state.messages.append({ 
        "role": "assistant", 
        "content": answer 
        })