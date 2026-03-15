from ollama import Client
from ..core.config import OLLAMA_BASE_URL, DEFAULT_MODEL
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from dataclasses import dataclass
from langchain.agents.structured_output import ToolStrategy

@dataclass
class AIResponse:
    """Response for AI"""
    title: str
    content: str

async def generate_response(context: str, query: str) -> AIResponse:

    prompt=f"""
    You are an expert AI assistant. Strictly use this context below to answer the user's question clearly and concisely with appropriate title.
    Context:
    {context}
    """

    llm = ChatOllama(
        base_url=OLLAMA_BASE_URL or "http://localhost:11434",
        model=DEFAULT_MODEL
    )

    agent = create_agent(
        model=llm,
        system_prompt=prompt,
        response_format=ToolStrategy(AIResponse)
    )

    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
    )

    return response["structured_response"]