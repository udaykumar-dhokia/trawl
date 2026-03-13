from ..core.config import CROSS_ENCODER
from typing import List

async def rerank_chunks(chunks: List[str], query: str, top_k = 5) -> List[str]:
    """
    Rerank a list of text chunks based on similarity to a query using a cross-encoder.

    Args:
        chunks (List[str]): List of text passages to rerank.
        query (str): The query string to compare against.
        top_k (int, optional): Number of top results to return. Defaults to 5.

    Returns:
        List[str]: Top-k reranked passages, sorted from most to least relevant.
    """

    pairs = [[query, passage] for passage in chunks]
    scores = CROSS_ENCODER.predict(pairs)
    reranked_pairs = [c for _, c in sorted(zip(scores, chunks), reverse=True)]

    return reranked_pairs[:top_k]