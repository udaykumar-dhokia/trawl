#!/usr/bin/env python3
"""
Example: Basic trawl usage

This example demonstrates how to use trawl programmatically
for research queries.
"""

import asyncio
from trawl.services.invoke_chat import invoke_chat


async def main():
    """Run a sample research query."""
    query = "Explain quantum computing in simple terms"

    print(f"Researching: {query}")
    print("-" * 50)

    try:
        # This will perform the research and print results
        await invoke_chat(query=query)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())