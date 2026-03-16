from datetime import datetime
from . import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Text, UUID, DateTime
from typing import List

class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    title = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.now())