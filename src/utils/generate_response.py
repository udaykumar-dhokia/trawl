from ollama import Client
from ..core.config import OLLAMA_BASE_URL, DEFAULT_MODEL

async def generate_response(context: str, query: str):

    prompt=f"""
    You are an expert AI assistant. Strictly use this context below to answer the question clearly and concisely.
    Context:
    {context}
    
    Question:
    {query}
    """

    client = Client(host=OLLAMA_BASE_URL if OLLAMA_BASE_URL else "https://localhost:11434")

    stream = client.chat(
        model=DEFAULT_MODEL,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        stream=True
    )


    for chunk in stream:
        print(chunk.message.content, end="", flush=True)