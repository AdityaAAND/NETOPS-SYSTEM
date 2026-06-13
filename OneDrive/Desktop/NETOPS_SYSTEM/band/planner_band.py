import asyncio
from thenvoi import Agent
from thenvoi.adapters import LangGraphAdapter
from thenvoi.config import load_agent_config
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

agent_id, api_key = load_agent_config("planner")

adapter = LangGraphAdapter(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    checkpointer=InMemorySaver(),
)

agent = Agent.create(
    adapter=adapter,
    agent_id=agent_id,
    api_key=api_key,
)

asyncio.run(agent.run())