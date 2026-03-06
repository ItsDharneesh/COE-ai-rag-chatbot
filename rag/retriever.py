from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

VECTOR_PATH = "vector_store"

def retrieve_docs(query):

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_db = FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    results = vector_db.similarity_search_with_score(query, k=3)

    docs = []
    scores = []

    for doc, score in results:
        docs.append(doc.page_content)
        scores.append(score)

    return docs, scores