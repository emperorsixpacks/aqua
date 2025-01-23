from langgraph.types import Command, interrupt
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from app.states import AgentState
import logging

logger = logging.getLogger("reviewer_node")
logger.setLevel(logging.INFO)

async def reviewer(state: AgentState):
    result = interrupt({
        "task": "Please review the strategy and provide instructions for improvement or approval.",
        "strategy": state.get("strategy_signals", "No strategy generated."),
    })

    user_instructions = result.get("review_instructions", "").strip()
    logger.info(f"User instructions received: {user_instructions}")
    state["review_instructions"] = user_instructions
    return state