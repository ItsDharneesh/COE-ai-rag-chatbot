import os
from pathlib import Path

import numpy as np
import streamlit as st
from dotenv import load_dotenv

from rag.generator import generate_answer
from rag.retriever import retrieve_docs
from rag.wiki_retriever import search_wikipedia

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
VECTOR_PATH = PROJECT_ROOT / "vector_store"


def _read_secret(name: str):
    try:
        return st.secrets.get(name)
    except Exception:
        return None


def ensure_openai_key() -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    secret_key = _read_secret("OPENAI_API_KEY")
    if secret_key:
        os.environ["OPENAI_API_KEY"] = secret_key
        return secret_key

    return None


def build_vector_store_on_demand() -> None:
    from rag.ingest import build_vector_store, chunk_documents, load_documents

    docs = load_documents()
    chunks = chunk_documents(docs)
    build_vector_store(chunks)


st.set_page_config(
    page_title="COE AI Assistant",
    page_icon=":robot_face:",
    layout="wide",
)

st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("About")
    st.write(
        """
This chatbot uses **Retrieval Augmented Generation (RAG)**.

**Sources used**
- Internal COE documents
- Wikipedia fallback

**Tech Stack**
- OpenAI GPT models
- OpenAI Embeddings
- FAISS Vector Store
- Streamlit UI
"""
    )

st.markdown('<div class="main-title">COE AI Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Ask questions about Lean, Six Sigma, KPI tracking and Operational Excellence</div>',
    unsafe_allow_html=True,
)

if not ensure_openai_key():
    st.error(
        "OPENAI_API_KEY is missing. Add it in Streamlit Cloud > App Settings > Secrets."
    )
    st.stop()

if not VECTOR_PATH.exists():
    st.warning(
        "Vector store not found. If this is Streamlit Cloud, either commit "
        "`vector_store/` to GitHub or click below to build it once."
    )
    if st.button("Build Vector Store"):
        try:
            with st.spinner("Building vector store from local_files..."):
                build_vector_store_on_demand()
            st.success("Vector store built. Click 'Rerun' in Streamlit.")
        except Exception as exc:
            st.error(f"Failed to build vector store: {exc}")
    st.stop()

query = st.chat_input("Ask something about Operational Excellence...")

if query:
    st.chat_message("user").write(query)

    try:
        with st.spinner("Searching documents and Wikipedia..."):
            docs, scores = retrieve_docs(query)

            confidence = float(np.mean(scores))
            threshold = 0.75

            source = "Documents"
            context_docs = docs

            if confidence > threshold:
                wiki_text = search_wikipedia(query)
                if wiki_text:
                    context_docs = [wiki_text]
                    source = "Wikipedia"

            answer = generate_answer(query, context_docs)
    except Exception as exc:
        st.error(f"Failed to process query: {exc}")
        st.stop()

    with st.chat_message("assistant"):
        st.markdown("### Answer")
        st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
        st.markdown(f"**Source Used:** `{source}`")

        st.markdown("### Confidence")
        confidence_score = min(1.0, max(0.0, 1 - confidence))
        st.progress(confidence_score)
        st.write(round(confidence_score, 2))

        st.markdown("### Retrieved Context")
        for i, doc in enumerate(context_docs):
            with st.expander(f"Source Chunk {i + 1}"):
                st.markdown(
                    f'<div class="source-box">{doc[:800]}</div>',
                    unsafe_allow_html=True,
                )
