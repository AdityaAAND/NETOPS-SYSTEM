import asyncio

from band_agents import Agent
from band_agents.adapters.langgraph import LangGraphAdapter

from graph.workflow import graph


async def main():

    adapter = LangGraphAdapter(
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