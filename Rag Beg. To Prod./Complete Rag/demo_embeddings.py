from google import genai
from google.genai import types
from dotenv import load_dotenv
import numpy as np


# Load environment variables from .env
load_dotenv()

# Create Gemini client
client = genai.Client()


# Documents
sentences = [
    "Python is widely used for artificial intelligence and machine learning.",
    "LangChain is a framework for building applications with large language models.",
    "Paris is the capital city of France.",
    "Vector databases are commonly used for semantic search."
]


# User query
query = "How can I build an AI application using Python?"


# --------------------------------------------------
# 1. Create embeddings for documents
# --------------------------------------------------

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=sentences, # type: ignore
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT"
    )
)

sentence_embeddings = [
    embedding.values # type: ignore
    for embedding in result.embeddings # type: ignore
]


# --------------------------------------------------
# 2. Create embedding for query
# --------------------------------------------------

query_result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query,
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_QUERY"
    )
)

query_embedding = query_result.embeddings[0].values # type: ignore


# --------------------------------------------------
# 3. Cosine similarity
# --------------------------------------------------

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


# --------------------------------------------------
# 4. Compare query with every document
# --------------------------------------------------

results = []

for sentence, embedding in zip(
    sentences,
    sentence_embeddings
):
    score = cosine_similarity(
        query_embedding,
        embedding
    )

    results.append(
        (sentence, score)
    )


# --------------------------------------------------
# 5. Sort by similarity
# --------------------------------------------------

results.sort(
    key=lambda x: x[1],
    reverse=True
)


# --------------------------------------------------
# 6. Display results
# --------------------------------------------------

print("\nQuery:")
print(query)

print("\nSimilarity Results:")

for sentence, score in results:
    print(f"{score:.4f} -> {sentence}")