import sys
import os


project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, project_root)



print("Tracing:",
      os.getenv("LANGCHAIN_TRACING"))

print("Project:",
      os.getenv("LANGCHAIN_PROJECT"))
from graph.workflow import graph

result = graph.invoke(
    {
        "alert":
        "CPU utilization 98% with OSPF neighbor resets",
        "tasks": [],
        "retrieved_docs": [],
        "diagnostics": [],
        "root_cause": "",
        "recommendation": ""
    }
)

print("FINAL STATE")
print("=" * 60)


print("\nTasks:")
print(result["tasks"])

print("\nRetrieved Documents:")
print(len(result["retrieved_docs"]))

print("\nDiagnostics:")
print(len(result["diagnostics"]))

print("\nROOT CAUSE ANALYSIS")
print("=" * 60)

print(
    result["root_cause"]
)

print("\nRecommendation:")
print(result["recommendation"])
