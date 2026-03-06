from functools import lru_cache
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VECTOR_PATH = PROJECT_ROOT / "vector_store"


@lru_cache(maxsize=1)
def _load_vector_db():
    if not VECTOR_PATH.exists():
        raise FileNotFoundError(
            f"Vector store not found at {VECTOR_PATH}. Build it with rag/ingest.py first."
        )

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.load_local(
        str(VECTOR_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def retrieve_docs(query, k=3):
    vector_db = _load_vector_db()
    results = vector_db.similarity_search_with_score(query, k=k)

    docs = []
    scores = []
    for doc, score in results:
        docs.append(doc.page_content)
        scores.append(float(score))

    return docs, scores
