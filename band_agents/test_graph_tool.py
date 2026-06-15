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

tool = graph_as_tool(
    graph=graph,
    name="netops_rca",
    description="Perform network root cause analysis",
    input_schema={
        "alert": str
    }
)

print(tool)