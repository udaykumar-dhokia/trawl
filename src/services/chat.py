from .search import search
from uuid import uuid1
from .process_url import process_url, ProcessUrlResult
from ..utils.retrieve import retrieve
from ..utils.rerank import rerank_chunks
from ..utils.generate_response import generate_response
import asyncio

async def chat(query: str):

    response_id = uuid1()

    urls = search(query)

    await asyncio.gather(
        *(process_url(url, response_id) for url in urls)
    )

    relevant_chunks = await retrieve(query=query, response_id=response_id)
    reranked_chunks = await rerank_chunks(query=query, chunks=relevant_chunks)

    context = "\n\n".join([f"{r}" for r in reranked_chunks])

    await generate_response(query=query, context=context)