from llm.llm_client import (
    LLMClient
)


class ReviewAgent:

    def __init__(self):

        self.llm = LLMClient()

    def analyze(
        self,
        alert,
        docs,
        diagnostics
    ):

        prompt = f"""
You are a senior network engineer.

Analyze the following alert.

ALERT:
{alert}

DOCUMENTS:
{docs}

DIAGNOSTICS:
{diagnostics}

Determine:

1. Root Cause
2. Confidence Score
3. Supporting Evidence

Provide a concise answer.
"""

        return self.llm.generate(
            prompt
        )
    
    