from langchain_core.messages import AIMessage
from langgraph.types import Command
from langgraph.graph import END
from typing import Dict

class StrategyAgent:
    async def generate_strategy(self, state: Dict) -> Command:
        """Strategy agent that generates an investment strategy."""

        messages = state.get("messages", [])
        risk_analysis = state.get("risk_analysis", "")

        strategy_message = f"Strategy based on risk analysis: {risk_analysis}. Suggested action: Buy with 70% allocation."

        messages.append(AIMessage(content=strategy_message))

        return Command(goto=END, update={"messages": messages})
