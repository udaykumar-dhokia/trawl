import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, CrossEncoder

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
SEARXNG_BASE_URL=os.getenv("SEARXNG_BASE_URL")
INDEX_PATH = "faiss_index.idx"
MODEL = SentenceTransformer("all-MiniLM-L6-v2")
CROSS_ENCODER = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")