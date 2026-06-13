from llm.llm_client import LLMClient


class DecisionAgent:
    def __init__(self):
        self.llm = LLMClient()
    def recommend(
            self,
            root_cause,

    ):
         prompt = f"""
You are a senior network operations engineer.

Based on the following Root Cause Analysis:

{root_cause}

Provide:

1. Recommended Fix
2. Priority (Low/Medium/High)
3. Validation Steps
4. Rollback Considerations

Be concise and practical.
"""
         return self.llm.generate(
             prompt
         )