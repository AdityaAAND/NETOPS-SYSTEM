from typing import TypedDict
from langgraph.graph import StateGraph

from agents.diagnostics_agent import DiagnosticAgent

agent = DiagnosticAgent()

class DiagnosticState(TypedDict, total=False):
    result: str


def diagnostic_node(state):

    diagnostics = agent.collect()

    return {
        "result": str(diagnostics)
    }


workflow = StateGraph(DiagnosticState)

workflow.add_node(
    "diagnostic",
    diagnostic_node
)

workflow.set_entry_point(
    "diagnostic"
)

graph = workflow.compile()