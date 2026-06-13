from typing import TypedDict, List

class NetOpsState(TypedDict):

    # Original alert
    alert: str

    tasks:List[str]

    # Documents from ChromaDB
    retrieved_docs: List[str]

    # Diagnostics output
    diagnostics: List[str]

    # RCA
    root_cause: str

    # Recommended action
    recommendation: str