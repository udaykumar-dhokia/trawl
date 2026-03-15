from .search import search
from uuid import uuid1
from .process_url import process_url, ProcessUrlResult
from ..utils.retrieve import retrieve
from ..utils.rerank import rerank_chunks
from ..utils.generate_response import generate_response
import asyncio
from sqlalchemy import UUID
from ..utils.insert_response import insert_response
from ..utils.insert_chat import insert_chat, update_chat_title

async def chat(query: str, chat_id: UUID = None, response_id: UUID = None):

    if chat_id is None:
        chat_id = await insert_chat()

    if response_id is None:
        response_id = uuid1()

    urls = search(query)

    await asyncio.gather(
        *(process_url(url, response_id) for url in urls)
    )

    relevant_chunks = await retrieve(query=query, response_id=response_id)
    reranked_chunks = await rerank_chunks(query=query, chunks=relevant_chunks)

    context = "\n\n".join([f"{r}" for r in reranked_chunks])

    content = await generate_response(query=query, context=context)

    await update_chat_title(chat_id=chat_id, title=content.title)
    await insert_response(response_id=response_id, query=query, content=content.content, chat_id=chat_id, urls=urls)

    print(content.content)