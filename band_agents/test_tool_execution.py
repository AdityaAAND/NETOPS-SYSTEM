import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, project_root)

from graph.workflow import graph
from band_agents.integrations.langgraph import graph_as_tool
import asyncio

tool = graph_as_tool(
    graph=graph,
    name="netops_rca",
    description="Perform network root cause analysis",
    input_schema={
        "alert": str
    }
)

async def main():

    result = await tool.ainvoke(
        {
            "alert":
            "CPU utilization 98% with OSPF adjacency resets"
        }
    )

    print(result)

asyncio.run(main())