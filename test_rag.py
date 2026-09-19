import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load FAISS index
index = faiss.read_index(
    "data/index/company_policy.index"
)


# Load the original text chunks
with open(
    "data/index/chunks.txt",
    "r",
    encoding="utf-8"
) as file:
    chunks = file.read().split("\n---CHUNK---\n")


# Customer question
question = "Can I return a product after 20 days?"


# Convert question into an embedding
query_embedding = model.encode(
    [question],
    convert_to_numpy=True
).astype("float32")


# Search for the 3 most relevant chunks
distances, indices = index.search(
    query_embedding,
    3
)


print("\nCustomer Question:")
print(question)

print("\nRelevant Knowledge:\n")

for i, index_position in enumerate(indices[0]):
    print(f"Result {i + 1}")
    print(chunks[index_position])
    print(f"Distance: {distances[0][i]:.4f}")
    print("-" * 60)