from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(query, docs):

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

        model="gpt-5.2",

        messages=[
            {"role": "user", "content": prompt}
        ],

        temperature=0.2
    )

    return response.choices[0].message.content