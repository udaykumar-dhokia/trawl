from sqlalchemy import UUID
from ..models.documents import DocumentChunk
from ..core.config import MODEL
from ..db.database import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

async def retrieve(query: str, response_id: UUID, top_k = 10) -> List[str]:
    """
    Retrieve the most relevant document chunks for a given query from the database.

    Args:
        query (str): The user's query string to search for.
        response_id (UUID): The UUID of the response/document to search within.
        top_k (int, optional): Maximum number of chunks to return. Defaults to 10.

    Returns:
        List[str]: A list of chunk texts ordered from most to least relevant.
    """

    query_embeddings = MODEL.encode(query).tolist()

    with Session(engine) as session:

        stmt = (
            select(DocumentChunk)
            .where(DocumentChunk.response_id == response_id)
            .order_by(DocumentChunk.embedding.cosine_distance(query_embeddings))
            .limit(top_k)
        )

        results = session.execute(stmt).scalars().all()

    return [r.chunk_text for r in results]