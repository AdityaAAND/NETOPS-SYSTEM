from agents.knowledge_agent import KnowledgeAgent
from agents.planner_agent import PlannerAgent
from agents.diagnostics_agent import DiagnosticAgent
from agents.review_agent import ReviewAgent
from agents.decision_agent import (
    DecisionAgent
)
from langchain_core.messages import AIMessage
import re

def get_alert(state):
    """Extract the network alert from API input or Band chat messages."""

    if state.get("alert"):
        return state["alert"]

    if state.get("messages"):

        msg = state["messages"][-1]

        text = (
            msg.content
            if hasattr(msg, "content")
            else str(msg)
        )

        text = re.sub(
            r'@\[\[.*?\]\]',
            '',
            text
        )

        return text.strip()

    raise KeyError(
        f"State keys received: {list(state.keys())}"
    )


decision_agent = (
    DecisionAgent()
)

agent = KnowledgeAgent()

def knowledge_node(state):
    """Retrieve relevant docs and incidents for the alert."""

    results = agent.retrieve_context(
        get_alert(state)
    )

    docs = []

    for doc in results:
        docs.append(doc.page_content)

    return {
        "retrieved_docs": docs
    }

planner_agent = PlannerAgent()

def planner_node(state):
    """Create an investigation plan for the incoming alert."""

    print("\n===== PLANNER STATE =====")
    print(type(state))
    print(state)
    print("=========================\n")

    tasks = planner_agent.plan(
        get_alert(state)
    )

    return{
        "tasks" : tasks
    }

diagnostics_agent = DiagnosticAgent()
def diagnostic_node(state):
    """Collect diagnostic command output used by the review step."""
    
    diagnostics = (diagnostics_agent.collect())
    return {
        "diagnostics":
        diagnostics
    }


review_agent = ReviewAgent()


def review_node(state):
    """Correlate alert, retrieved knowledge, and diagnostics into an RCA."""

    analysis = review_agent.analyze(
        get_alert(state),
        state["retrieved_docs"],
        state["diagnostics"]
    )

    return {
        "root_cause": analysis
    }


decision_agent = DecisionAgent()

def decision_node(state):
    """Generate the final remediation recommendation from the RCA."""

    recommendation = decision_agent.recommend(
        state["root_cause"]
    )

    print("\n===== FINAL RECOMMENDATION =====")
    print(recommendation)
    print("===============================\n")

    return {
        "recommendation": recommendation
    }

def response_node(state):
    """Format the final RCA state as a LangChain AIMessage."""

    return {
        "messages": [
            AIMessage(
                content=f"""
NETWORK RCA REPORT

Alert:
{get_alert(state)}

Root Cause:
{state['root_cause']}

Recommendation:
{state['recommendation']}
"""
            )
        ]
    }
