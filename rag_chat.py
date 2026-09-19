import faiss
from sentence_transformers import SentenceTransformer
from ollama import chat


# --------------------------------------------------
# 1. Load embedding model
# --------------------------------------------------

print("Loading AI knowledge system...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 2. Load FAISS knowledge base
# --------------------------------------------------

index = faiss.read_index(
    "data/index/company_policy.index"
)


# --------------------------------------------------
# 3. Load knowledge chunks
# --------------------------------------------------

with open(
    "data/index/chunks.txt",
    "r",
    encoding="utf-8"
) as file:

    chunks = file.read().split(
        "\n---CHUNK---\n"
    )


print("Knowledge base loaded successfully.")


# --------------------------------------------------
# 4. Customer support chatbot
# --------------------------------------------------

print("\n" + "=" * 60)
print("AI CUSTOMER SUPPORT CHATBOT")
print("=" * 60)

print("\nYou can ask questions about:")
print("- Returns")
print("- Refunds")
print("- Order cancellation")
print("- Delivery")
print("- Damaged products")

print("\nType 'exit' to close the chatbot.")

print("=" * 60)


while True:

    # --------------------------------------------------
    # Get customer question
    # --------------------------------------------------

    question = input("\nCustomer: ").strip()


    # --------------------------------------------------
    # Exit chatbot
    # --------------------------------------------------

    if question.lower() in ["exit", "quit"]:

        print("\nThank you for contacting customer support!")

        break


    # --------------------------------------------------
    # Ignore empty questions
    # --------------------------------------------------

    if not question:

        print("Please enter a question.")

        continue


    # --------------------------------------------------
    # Convert question into embedding
    # --------------------------------------------------

    query_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")


    # --------------------------------------------------
    # Search knowledge base
    # --------------------------------------------------

    distances, indices = index.search(
        query_embedding,
        3
    )


    # --------------------------------------------------
    # Retrieve relevant company information
    # --------------------------------------------------

    retrieved_context = "\n\n".join(
        chunks[i]
        for i in indices[0]
    )


    # --------------------------------------------------
    # Send question + knowledge to Qwen
    # --------------------------------------------------

    response = chat(

        model="qwen2.5:3b",

        messages=[

            {
                "role": "system",

                "content": """
You are a professional AI customer support agent.

Answer the customer's question using ONLY the
company information provided in the context.

Important rules:

1. Do not invent company policies.
2. Do not invent order status.
3. Do not invent refund status.
4. Do not invent delivery status.
5. Carefully interpret numbers and time periods.
6. If the customer asks whether something is allowed,
   compare their situation with the policy conditions.
7. If the answer cannot be determined from the
   company information, say that the issue should
   be escalated to a human support agent.

Give a clear, professional and concise response.
"""
            },

            {
                "role": "user",

                "content": f"""
Company Knowledge:

{retrieved_context}


Customer Question:

{question}
"""
            }

        ]
    )


    # --------------------------------------------------
    # Display AI response
    # --------------------------------------------------

    print("\nAI Support Agent:")
    print(response.message.content)