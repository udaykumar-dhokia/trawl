from uuid import uuid1
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from ..db.database import engine
from ..models.documents import Document

async def insert_document(response_id: UUID, content: str) -> UUID:
    """
    Insert a new document into the database and return its unique ID.

    Args:
        response_id (UUID): The UUID of the response or parent entity this document belongs to.
        content (str): The textual content of the document to be stored.

    Returns:
        UUID: The unique identifier of the newly created document.
    """

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