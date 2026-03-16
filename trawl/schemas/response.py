import uuid
from pydantic import BaseModel
from typing import List
from datetime import datetime

class Response(BaseModel):
    id: uuid.UUID
    vector_id: uuid.UUID
    query: str
    sources: List[str]
    response: str
    created_at: datetime