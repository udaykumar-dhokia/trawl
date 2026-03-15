import argparse
import asyncio
import uvicorn
from src.main import app
from src.services.chat import chat
import truststore

async def main():
    parser = argparse.ArgumentParser(description="searchx")
    parser.add_argument("--q", type=str, help="Your query")
    args = parser.parse_args()

    if args.q:
        query = args.q
        await chat(query=query)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    truststore.inject_into_ssl()
    asyncio.run(main())