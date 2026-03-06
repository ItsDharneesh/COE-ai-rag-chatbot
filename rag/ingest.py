import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "local_files"
VECTOR_PATH = PROJECT_ROOT / "vector_store"
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)


def load_documents():

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_PATH}")

    documents = []

    for file in DATA_PATH.iterdir():
        if not file.is_file():
            continue
        if file.suffix.lower() == ".txt":
            loader = TextLoader(str(file))
        elif file.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file))
        else:
            continue
        documents.extend(loader.load())

    if not documents:
        raise ValueError(
            f"No .txt or .pdf files found in data directory: {DATA_PATH}"
        )

    return documents


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)


def build_vector_store(chunks):

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            f"OPENAI_API_KEY is missing. Set it in your environment or in {ENV_PATH}."
        )

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_db = FAISS.from_documents(chunks, embeddings)

    vector_db.save_local(str(VECTOR_PATH))

    print("Vector DB built successfully")


if __name__ == "__main__":

    docs = load_documents()

    chunks = chunk_documents(docs)

    build_vector_store(chunks)
