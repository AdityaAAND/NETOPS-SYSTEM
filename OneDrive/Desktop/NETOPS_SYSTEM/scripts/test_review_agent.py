 
import sys
import os

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, project_root)



from agents.review_agent import (
    ReviewAgent
)

agent = ReviewAgent()

result = agent.analyze(
    alert=
    "CPU utilization 98% with OSPF neighbor resets",

    docs=
    "Historical OSPF routing loop incident",

    diagnostics=
    "CPU 98%, adjacency resets"
)

print(result)