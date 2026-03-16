from .chat import chat
from sqlalchemy import UUID
from dataclasses import dataclass
from ..utils.spawn_agent import spawn_agent
from typing import AsyncGenerator
from ..utils.event import event

@dataclass
class AIResponse:
    """Response from AI"""
    enhanced_query: str

async def invoke_chat(query: str, chat_id: UUID = None, response_id: UUID = None) -> AsyncGenerator[str, None]:
    prompt ="""
        Generate a precise and optimized search engine query that will return the most relevant and high-quality results.
    
        Guidelines:
        - Use important keywords from the request
        - Remove unnecessary words
        - Keep it concise and search-friendly
    
        User request:
        """

    yield event("status", message="Enhancing your query...")
    agent = spawn_agent(prompt, AIResponse)

    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
    )

    enhanced_query = response["structured_response"].enhanced_query

    async for chunk in chat(enhanced_query, chat_id, response_id):
        yield chunk