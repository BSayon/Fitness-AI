from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from src.model.model import llm
from src.prompts.prompt import SYSTEM_PROMPT

# An in-memory checkpointer gives the agent short-term conversational memory.
# Each user/feature gets an isolated conversation via a distinct `thread_id`
# passed in the invocation config (see src/service/service.py).
checkpointer = InMemorySaver()

agent = create_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)