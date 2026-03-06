import os

from openai import OpenAI


def generate_answer(query, docs):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is missing.")

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    context = "\n\n".join(docs)

    prompt = f"""
You are an expert assistant answering questions about Lean, Six Sigma,
operational excellence, and KPI tracking.

Use the provided context to answer the question.

Context:
{context}

Question:
{query}

Answer clearly and concisely.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content
