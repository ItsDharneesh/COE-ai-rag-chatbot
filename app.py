import streamlit as st
import numpy as np
import os

from dotenv import load_dotenv
load_dotenv()

# RAG modules
from rag.wiki_retriever import search_wikipedia
from rag.retriever import retrieve_docs
from rag.generator import generate_answer
from rag.ingest import load_documents, chunk_documents, build_vector_store


# -------------------------------------------------
# BUILD VECTOR STORE IF MISSING (FOR CLOUD DEPLOYMENT)
# -------------------------------------------------

if not os.path.exists("vector_store"):
    docs = load_documents()
    chunks = chunk_documents(docs)
    build_vector_store(chunks)


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="COE AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# -------------------------------------------------
# CUSTOM STYLING
# -------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size:40px;
    font-weight:700;
    color:#EAECEE;
}

.subtitle {
    color:#AAB7B8;
    margin-bottom:30px;
}

.answer-box {
    background-color:#1E1E1E;
    padding:20px;
    border-radius:10px;
    border-left:5px solid #2E86C1;
    color:#FFFFFF;
    font-size:16px;
}

.source-box {
    background-color:#1E1E1E;
    padding:15px;
    border-radius:8px;
    border:1px solid #2C3E50;
    color:#FFFFFF;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.title("About")

    st.write("""
This chatbot uses **Retrieval Augmented Generation (RAG)**.

**Sources used**
- Internal COE documents
- Wikipedia fallback

**Tech Stack**
- OpenAI GPT-5.2
- OpenAI Embeddings
- FAISS Vector Store
- Streamlit UI
""")


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown(
    '<div class="main-title">COE AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions about Lean, Six Sigma, KPI tracking and Operational Excellence</div>',
    unsafe_allow_html=True
)


# -------------------------------------------------
# CHAT INPUT
# -------------------------------------------------

query = st.chat_input("Ask something about Operational Excellence...")


# -------------------------------------------------
# QUERY PROCESSING
# -------------------------------------------------

if query:

    st.chat_message("user").write(query)

    with st.spinner("🏃 Searching documents and Wikipedia..."):

        docs, scores = retrieve_docs(query)

        confidence = float(np.mean(scores))
        threshold = 0.75

        source = "Documents"
        context_docs = docs

        # Wikipedia fallback if similarity weak
        if confidence > threshold:

            wiki_text = search_wikipedia(query)

            if wiki_text:
                context_docs = [wiki_text]
                source = "Wikipedia"

        answer = generate_answer(query, context_docs)


    # -------------------------------------------------
    # ANSWER DISPLAY
    # -------------------------------------------------

    with st.chat_message("assistant"):

        st.markdown("### 🤖 Answer")

        st.markdown(
            f'<div class="answer-box">{answer}</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"**Source Used:** `{source}`")


        # -------------------------------------------------
        # CONFIDENCE SCORE
        # -------------------------------------------------

        st.markdown("### Confidence")

        confidence_score = min(1.0, max(0.0, 1 - confidence))

        st.progress(confidence_score)

        st.write(round(confidence_score, 2))


        # -------------------------------------------------
        # RETRIEVED CONTEXT
        # -------------------------------------------------

        st.markdown("### Retrieved Context")

        for i, doc in enumerate(context_docs):

            with st.expander(f"Source Chunk {i+1}"):

                st.markdown(
                    f'<div class="source-box">{doc[:800]}</div>',
                    unsafe_allow_html=True
                )