from ..models.response import Response
from sqlalchemy.orm import Session
from ..db.database import engine
from sqlalchemy import UUID
from typing import List

async def insert_response(response_id: UUID, query: str, urls: List[str], image_urls: List[str], content: str, chat_id: UUID):
    with Session(engine) as session:
        response = Response(
            id=response_id,
            query=query,
            sources=urls,
            image_urls=image_urls,
            response=content,
            chat_id=chat_id
        )

        session.add(response)
        session.commit()