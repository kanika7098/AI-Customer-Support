from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# 1. Load the company document
# --------------------------------------------------

document_path = Path("data/documents/company_policy.txt")

text = document_path.read_text(encoding="utf-8")


# --------------------------------------------------
# 2. Split the document into smaller chunks
# --------------------------------------------------

chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]

print(f"Loaded {len(chunks)} knowledge chunks.")


# --------------------------------------------------
# 3. Load the embedding model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# 4. Convert text chunks into embeddings
# --------------------------------------------------

embeddings = model.encode(
    chunks,
    convert_to_numpy=True
).astype("float32")


# --------------------------------------------------
# 5. Create FAISS index
# --------------------------------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


# --------------------------------------------------
# 6. Create output directory
# --------------------------------------------------

Path("data/index").mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 7. Save FAISS index
# --------------------------------------------------

faiss.write_index(
    index,
    "data/index/company_policy.index"
)


# --------------------------------------------------
# 8. Save the text chunks
# --------------------------------------------------

with open(
    "data/index/chunks.txt",
    "w",
    encoding="utf-8"
) as file:

    for chunk in chunks:
        file.write(chunk)
        file.write("\n---CHUNK---\n")


print("\nKnowledge base created successfully!")
print(f"Number of chunks: {len(chunks)}")
print(f"Embedding dimensions: {dimension}")