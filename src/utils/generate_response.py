from dataclasses import dataclass
from ..utils.spawn_agent import spawn_agent
from typing import AsyncGenerator
from .event import event

@dataclass
class AIResponse:
    """Response from AI"""
    title: str
    content: str

async def generate_response(context: str, query: str) -> AsyncGenerator[str, None]:

    prompt=f"""
    You are an expert AI assistant. Strictly use this context below to answer the user's question clearly and concisely with appropriate title.
    Context:
    {context}
    """

    yield event("status", message="Thinking...")
    agent = spawn_agent(prompt, AIResponse)

    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
    )

    result: AIResponse = response["structured_response"]

    yield event("title", text=result.title)
    yield event("content", text=result.content)