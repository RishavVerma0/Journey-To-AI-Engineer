"""CLI chat loop. Run `python ingest.py` first if you haven't already.

    python main.py
"""

import asyncio
from llama_index.core.workflow import Context

from agent import build_agent


async def chat():
    agent = build_agent()
    ctx = Context(agent)  # keeps conversation memory across turns

    print("Maruti assistant ready. Type 'exit' to quit.\n")
    while True:
        query = input("You: ").strip()
        if not query:
            continue
        if query.lower() in ("exit", "quit"):
            break
        try:
            response = await agent.run(query, ctx=ctx)
            print(f"Assistant: {response}\n")
        except Exception as e:
            print(f"[Error] {e}\n")


if __name__ == "__main__":
    asyncio.run(chat())