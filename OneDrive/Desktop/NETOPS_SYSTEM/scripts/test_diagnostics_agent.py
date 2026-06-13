import os
import sys

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, project_root)



from agents.diagnostics_agent import (
    DiagnosticAgent
)

agent = DiagnosticAgent()

results = agent.collect()

print(
    f"Loaded {len(results)} diagnostics"
)

for i, result in enumerate(
    results,
    start=1
):

    print(
        f"\nDiagnostic {i}"
    )

    print(
        "-" * 50
    )

    print(
        result[:200]
    )