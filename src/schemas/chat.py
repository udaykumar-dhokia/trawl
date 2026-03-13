from datetime import datetime
from typing import List
from pydantic import BaseModel
from sqlalchemy import UUID

class Chat(BaseModel):
    id : UUID
    title : str
    responses : List[UUID]
    created_at : datetime
    updated_at : datetime