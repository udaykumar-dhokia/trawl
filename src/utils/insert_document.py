from uuid import uuid1
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from db.database import engine
from models.documents import Document

async def insert_document(response_id: UUID, content: str) -> UUID:

    document_id = uuid1()

    with Session(engine) as session:
        doc = Document(
            id=document_id,
            content=content,
            response_id=response_id,
        )

        session.add(doc)
        session.commit()

    return document_id