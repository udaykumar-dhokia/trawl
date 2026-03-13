from sqlalchemy import UUID
from pydantic import BaseModel
from typing import List

class Document(BaseModel):
    id: UUID
    response_id: UUID
    content: str

class DocumentChunk(BaseModel):
    id: UUID
    document_id: UUID
    response_id: UUID
    chunk_text: str
    embedding: List[float]