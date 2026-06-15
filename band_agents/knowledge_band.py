from typing import TypedDict, List, Any
from langgraph.graph import StateGraph

from agents.knowledge_agent import KnowledgeAgent

agent = KnowledgeAgent()

class KnowledgeState(TypedDict, total=False):
    messages: List[Any]
    result: str


def knowledge_node(state):

    msg = state["messages"][-1]

    query = (
        msg.content
        if hasattr(msg, "content")
        else str(msg)
    )

    docs = agent.retrieve_context(query)

    results = [
        doc.page_content
        for doc in docs
    ]

    return {
        "result": "\n\n".join(results)
    }


workflow = StateGraph(KnowledgeState)

workflow.add_node(
    "knowledge",
    knowledge_node
)

workflow.set_entry_point(
    "knowledge"
)

graph = workflow.compile()