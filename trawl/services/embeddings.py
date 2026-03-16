from sentence_transformers import SentenceTransformer
from ..core.config import MODEL

async def create_embeddings(chunk):
    return MODEL.encode(chunk)