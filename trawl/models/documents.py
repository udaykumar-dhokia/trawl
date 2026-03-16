from sqlalchemy import Column, Text, UUID
from pgvector.sqlalchemy import Vector
from . import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    response_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(Text)

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    document_id = Column(UUID(as_uuid=True), nullable=False)
    response_id = Column(UUID(as_uuid=True), nullable=False)
    chunk_text = Column(Text)
    embedding = Column(Vector(384))