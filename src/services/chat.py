from .search import search
from uuid import uuid1
from typing import List
from .process_url import process_url, ProcessUrlResult
from concurrent.futures import ThreadPoolExecutor, as_completed

async def chat(query: str):

    response_id = uuid1()

    urls = search(query)

    processed_urls: List[ProcessUrlResult] = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_url, url, response_id): url for url in urls}

        for future in as_completed(futures):
            processed_urls.append(future.result())