from langgraph.types import Command, interrupt
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from src.states import AgentState
import logging

logger = logging.getLogger("reviewer_node")
logger.setLevel(logging.INFO)
async def reviewer(state: AgentState) -> Command:
    try:
        human_message = interrupt({
            "question": "Please review the generated strategy and provide feedback or approve to deploy.",
            "strategy": state.get("strategy_signals", "No strategy generated yet.")
        })
        logger.info(f"Human review input received: {human_message}")

        state.setdefault("messages", []).append(
            HumanMessage(content=human_message)
        )

        if "approve" in human_message.lower():
            logger.info("Human approved the strategy. Proceeding to deployment.")
            return Command(goto="deploy", update={"review_feedback": human_message})
        else:
            logger.info("Human requested changes. Routing back to strategy generation.")
            return Command(goto="generate_strategy", update={"review_feedback": human_message})

    except Exception as e:
        logger.error(f"Error in reviewer: {e}", exc_info=True)
        state.setdefault("messages", []).append(
            AIMessage(content="An error occurred while processing your review. Please try again."))
        return Command(goto="error_handler")