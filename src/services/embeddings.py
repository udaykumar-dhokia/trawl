from sentence_transformers import SentenceTransformer, CrossEncoder

async def create_embeddings(chunk):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(chunk)