from uuid import uuid1
from sqlalchemy.orm import Session
from db.database import engine
from sqlalchemy import UUID
from typing import List
from models.documents import DocumentChunk

async def batch_insert_embeddings(chunk_texts: List[str], response_id: UUID, document_id: UUID, embeddings: List[List[float]]) -> List[UUID]:

    document_chunk_ids = []

    with Session(engine) as session:
        docs = []

        for text, embeddings in zip(chunk_texts, embeddings):
            document_chunk_id = uuid1()
            document_chunk_ids.append(document_chunk_id)

            docs.append(DocumentChunk(
                id=document_chunk_id,
                document_id=document_id,
                response_id=response_id,
                chunk_text=text,
                embedding=embeddings
            ))

        session.add_all(docs)
        session.commit()

    return document_chunk_ids