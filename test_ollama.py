from ollama import chat

response = chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "system",
            "content": "You are a professional AI customer support agent for an e-commerce company."
        },
        {
            "role": "user",
            "content": "A customer says: My order has not arrived yet. What should I do?"
        }
    ]
)

print("\nAI Customer Support:")
print(response.message.content)