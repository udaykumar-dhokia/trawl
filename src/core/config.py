import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, CrossEncoder
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from ..utils.config_manager import ConfigManager

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SEARXNG_BASE_URL = os.getenv("SEARXNG_BASE_URL")
API_BASE = os.getenv("API_BASE")
INDEX_PATH = "faiss_index.idx"
MODEL = SentenceTransformer("all-MiniLM-L6-v2")
CROSS_ENCODER = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def get_llm():
    """Retrieve LLM based on ConfigManager or fallback to .env"""
    config = ConfigManager.get_config()
    provider = config.get("provider")
    
    if provider == "google":
        api_key = config.get("google_api_key") or os.getenv("GOOGLE_API_KEY")
        model = config.get("model") or os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
        if api_key:
            return ChatGoogleGenerativeAI(model=model, google_api_key=api_key)
    
    base_url = config.get("ollama_base_url") or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = config.get("model") or os.getenv("DEFAULT_MODEL", "llama3")
    return ChatOllama(base_url=base_url, model=model)