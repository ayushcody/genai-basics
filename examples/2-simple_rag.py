"""A complete RAG pipeline, no vector database. (Chapter 3)

Pipeline: chunk -> embed -> store -> retrieve -> augment -> generate.
For real projects, swap the in-memory list for FAISS, pgvector, or Chroma.

Run:
    pip install -r requirements.txt
    export OPENAI_API_KEY="your-key-here"
    export OPENAI_MODEL="a-current-chat-model"
    python simple_rag.py
"""

import os

import numpy as np
from openai import OpenAI

client = OpenAI()

# Set OPENAI_MODEL to a chat model your account can use; model availability changes
# over time, so check platform.openai.com/docs/models for what is live.
MODEL = os.environ.get("OPENAI_MODEL")
if not MODEL:
    raise SystemExit("Set OPENAI_MODEL first, e.g. export OPENAI_MODEL=<a current chat model>")

# --- 1. Source text (pretend this came from files) ---
SOURCE_TEXT = """
The library is open Monday to Friday, 9 AM to 8 PM. On Saturdays it opens at 10 AM
and closes at 4 PM. It is closed on Sundays.

Students can borrow up to 5 books at a time for 14 days. Renewals are allowed once,
unless another student has reserved the book.

Late returns are charged 2 rupees per book per day. Unpaid fines over 100 rupees
block new borrowings until cleared.
""".strip()


# --- 2. Chunk: group paragraphs toward a soft max_chars target ---
# A single oversized paragraph is kept intact, so it can exceed the target.
def chunk(text, max_chars=200):
    chunks, current = [], ""
    for passage in (p.strip() for p in text.split("\n\n") if p.strip()):
        candidate = f"{current}\n\n{passage}".strip()
        if current and len(candidate) > max_chars:
            chunks.append(current)
            current = passage
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


DOCUMENTS = chunk(SOURCE_TEXT)  # three small passages in this demo


# --- 3 + 4. Embed and store ---
def embed(texts):
    resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return np.array([item.embedding for item in resp.data])


chunk_vectors = embed(DOCUMENTS)  # in a real system this goes into a vector DB


def cosine_similarity(a, b):
    return (a @ b.T) / (np.linalg.norm(a, axis=1, keepdims=True) * np.linalg.norm(b, axis=1))


# --- 5. Retrieve ---
def retrieve(question, top_k=2):
    q = embed([question])
    scores = cosine_similarity(q, chunk_vectors)[0]
    best = np.argsort(scores)[::-1][:top_k]
    return [DOCUMENTS[i] for i in best]


# --- 6 + 7. Augment and generate ---
def answer(question):
    chunks = retrieve(question)
    context = "\n\n".join(f"<chunk>\n{c}\n</chunk>" for c in chunks)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Answer using only the context below. "
                "If the answer is not in the context, say you do not know.\n\n" + context,
            },
            {"role": "user", "content": question},
        ],
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    for q in [
        "When is the library open on weekends?",
        "How much is the late fee?",
        "What is the wifi password?",  # not in the docs: check whether it declines to invent an answer
    ]:
        print(f"Q: {q}\nA: {answer(q)}\n")
