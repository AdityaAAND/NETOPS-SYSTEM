import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))


import asyncio

from band import Agent
from band_reply_adapter import ReplyingLangGraphAdapter
from graph.workflow import graph


async def main():
    """Start the NetOps Band agent using the reply-capable LangGraph adapter."""

    # This adapter posts the final LangGraph report back to the chat room.
    adapter = ReplyingLangGraphAdapter(
        graph=graph
    )

    agent = Agent.from_config(
        "netops",
        adapter=adapter
    )

    print("NetOps RCA Agent Running...")

    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())

