from langchain.agents import create_agent
from ..core.config import get_llm
from langchain.agents.structured_output import ToolStrategy

def spawn_agent(prompt: str = "", ai_response = None):
    return create_agent(
        model=get_llm(),
        system_prompt=prompt,
        response_format=ToolStrategy(ai_response) if ai_response else None,
    )