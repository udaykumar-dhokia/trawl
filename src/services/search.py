import httpx
from dotenv import load_dotenv
from typing import List, Tuple
from ..core.config import SEARXNG_BASE_URL

load_dotenv()

async def search(query: str, image_query: str) -> Tuple[List[str], List[str]]:
    """Search for the relevant websites asynchronously"""

    if not SEARXNG_BASE_URL:
        return []
    
    web_search_params = {
        "q": query,
        "format": "json"
    }

    image_search_params={
        "q": image_query,
        "categories": "images",
        "format": "json"
    }

    async with httpx.AsyncClient() as client:
        web_response = await client.get(url=f"{SEARXNG_BASE_URL}/search", params=web_search_params)
        image_response = await client.get(url=f"{SEARXNG_BASE_URL}/search", params=image_search_params)
        web_data = web_response.json()
        image_data = image_response.json()

    urls = [r["url"] for r in web_data["results"][:15]]
    image_urls = [r["img_src"] for r in image_data["results"][:5]]

    return urls, image_urls