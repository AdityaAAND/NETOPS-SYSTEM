
import sys
import os

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, project_root)

from agents.knowledge_agent import KnowledgeAgent

agent = KnowledgeAgent()

results = agent.retrieve_context(
    "CPU utilization 98% with OSPF neighbor resets"
)

for i, doc in enumerate(results, start=1):

    print(f"\nResult {i}")

    print("-" * 60)

    print(
        "Source:",
        doc.metadata.get(
            "source",
            "Unknown"
        )
    )

    print()

    print(
        doc.page_content[:250]
    )

    print()