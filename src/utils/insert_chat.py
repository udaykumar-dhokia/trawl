from sqlalchemy.orm import Session
from ..db.database import engine
from sqlalchemy import UUID
from ..models.chat import Chat
from uuid import uuid1

async def insert_chat() -> UUID:

    chat_id = uuid1()

    with Session(engine) as session:
        chat = Chat(
            id=chat_id,
        )

        session.add(chat)
        session.commit()

    return chat_id

async def update_chat_title(chat_id: UUID, title: str):
    with Session(engine) as session:
        chat = session.get(Chat, chat_id)

        if chat and not chat.title:
            chat.title = title
            session.commit()

        return chat