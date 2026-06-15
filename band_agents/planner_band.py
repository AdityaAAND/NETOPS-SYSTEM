import asyncio

from band_agents import Agent
from band_agents.adapters.langgraph import LangGraphAdapter
from langgraph.graph import StateGraph
from typing import TypedDict

from agents.planner_agent import PlannerAgent


class PlannerState(TypedDict, total=False):
    messages: list
    result: str


planner = PlannerAgent()


def planner_node(state):

    msg = state["messages"][-1]

    alert = msg.content if hasattr(msg, "content") else str(msg)

    result = planner.plan(alert)

    return {"result": str(result)}


workflow = StateGraph(PlannerState)

workflow.add_node("planner", planner_node)
workflow.set_entry_point("planner")

graph = workflow.compile()


async def main():

    adapter = LangGraphAdapter(graph=graph)

    agent = Agent.from_config(
        "planner",
        adapter=adapter
    )

    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())