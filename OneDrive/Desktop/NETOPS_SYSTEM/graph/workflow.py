from langgraph.graph import StateGraph
from graph.state import NetOpsState
from graph.nodes import knowledge_node
from graph.nodes import planner_node
from graph.nodes import diagnostic_node
from graph.nodes import review_node
from graph.nodes import decision_node

workflow = StateGraph(NetOpsState)

workflow.add_node(
    "planner",
    planner_node
)
workflow.add_node(
    "knowledge",
    knowledge_node
)


workflow.add_node(
    "diagnostic",
    diagnostic_node
)

workflow.add_node(
    "review",
    review_node
)

workflow.add_node(
    "decision",
    decision_node
)
workflow.set_entry_point(
    "planner"
)


workflow.add_edge(
    "planner",
    "knowledge",
    
)
workflow.add_edge(
    "knowledge",
    "diagnostic"
)

workflow.add_edge(
    "diagnostic",
    "review"
)

workflow.add_edge(
    "review",
    "decision"
)
graph = workflow.compile()