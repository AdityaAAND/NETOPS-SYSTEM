import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, project_root)

from agents.decision_agent import (
    DecisionAgent
)

agent = DecisionAgent()

result = agent.recommend(
    """
Root Cause:
OSPF Routing Loop

Confidence:
85%

Evidence:
CPU utilization 98%
Adjacency resets
"""
)

print(result)