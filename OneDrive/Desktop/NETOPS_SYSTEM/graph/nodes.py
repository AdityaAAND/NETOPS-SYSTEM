from agents.knowledge_agent import KnowledgeAgent
from agents.planner_agent import PlannerAgent
from agents.diagnostics_agent import DiagnosticAgent
from agents.review_agent import ReviewAgent
from agents.decision_agent import (
    DecisionAgent
)

decision_agent = (
    DecisionAgent()
)

agent = KnowledgeAgent()

def knowledge_node(state):

    results = agent.retrieve_context(
        state["alert"]
    )

    docs = []

    for doc in results:
        docs.append(doc.page_content)

    return {
        "retrieved_docs": docs
    }

planner_agent = PlannerAgent()

def planner_node(state):

    tasks = planner_agent.plan(
        state["alert"]
    )

    return{
        "tasks" : tasks
    }

diagnostics_agent = DiagnosticAgent()
def diagnostic_node(state):
    
    diagnostics = (diagnostics_agent.collect())
    return {
        "diagnostics":
        diagnostics
    }


review_agent = ReviewAgent()


def review_node(state):

    analysis = review_agent.analyze(
        state["alert"],
        state["retrieved_docs"],
        state["diagnostics"]
    )

    return {
        "root_cause": analysis
    }


decision_agent = DecisionAgent()

def decision_node(state):

    recommendation = (
        decision_agent.recommend(
            state["root_cause"]
        )
    )

    return {
        "recommendation":
        recommendation
    }