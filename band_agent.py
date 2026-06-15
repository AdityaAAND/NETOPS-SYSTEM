
import asyncio

from band import Agent
from band_reply_adapter import ReplyingLangGraphAdapter
from graph.workflow import graph


async def main():
    """Start the Band NetOps agent and connect chat messages to LangGraph."""

    # The adapter is responsible for invoking LangGraph and sending the reply.
    adapter = ReplyingLangGraphAdapter(
        graph=graph
    )

    # Load the NetOps Band agent credentials from agent_config.yaml.
    agent = Agent.from_config(
        "netops",
        adapter=adapter
    )

    print("NetOps RCA Band Agent Running...")
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())

