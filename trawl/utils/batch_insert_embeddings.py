from uuid import uuid1
from sqlalchemy.orm import Session
from ..db.database import engine
from sqlalchemy import UUID
from typing import List
from ..models.documents import DocumentChunk

async def batch_insert_embeddings(chunk_texts: List[str], response_id: UUID, document_id: UUID, embeddings: List[List[float]]) -> List[UUID]:
    """
    Batch insert multiple document chunks with their embeddings into the database.

    Args:
        chunk_texts (List[str]): List of textual chunks to store.
        response_id (UUID): The UUID of the response or parent entity the chunks belong to.
        document_id (UUID): The UUID of the document these chunks belong to.
        embeddings (List[List[float]]): Precomputed embeddings for each chunk.

    Returns:
        List[UUID]: A list of UUIDs for each inserted DocumentChunk, in the same order as the input.
    """

    document_chunk_ids = []

    with Session(engine) as session:
        docs = []

        for text, embedding in zip(chunk_texts, embeddings):
            document_chunk_id = uuid1()
            document_chunk_ids.append(document_chunk_id)

            docs.append(DocumentChunk(
                id=document_chunk_id,
                document_id=document_id,
                response_id=response_id,
                chunk_text=text,
                embedding=embedding
            ))

        session.add_all(docs)
        session.commit()

    return document_chunk_ids