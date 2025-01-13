from langchain_openai import ChatOpenAI
from langgraph.types import Command
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from src.services.market_service import MarketService
import logging
from typing import Dict

logger = logging.getLogger("RiskAgent")
logger.setLevel(logging.INFO)

class RiskAgent:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
        self.system_instructions = SystemMessage(content="""You are a risk assessment expert. Your role is to:
        - Analyze market conditions and performance metrics
        - Calculate the overall risk level based on market trends and historical performance
        - Determine whether the risk is low, medium, or high based on predefined thresholds
        - Provide a risk assessment report, including actionable insights for managing risk.""")

    async def assess_risk(self, state: Dict) -> Command:
        try:
            market_analysis = state.get("market_analysis", {})
            performance_metrics = state.get("performance_metrics", {})

            logger.info(f"Received market analysis and performance metrics: {market_analysis}, {performance_metrics}")

            messages = [
                self.system_instructions,
                HumanMessage(content=f"""Please assess the risk based on the following data:
                Market Analysis: {market_analysis}
                Performance Metrics: {performance_metrics}
                Provide a risk level of Low, Medium, or High based on the analysis.""")
            ]

            analysis_response = await self.model.ainvoke(messages)
            logger.info(f"Risk analysis completed: {analysis_response}")

            messages = state.get("messages", [])
            messages.append(AIMessage(content=f"Risk analysis report: {analysis_response}"))

            return Command(goto="strategy_agent", update={"messages": messages, "risk_analysis": {"level": analysis_response}})

        except Exception as e:
            logger.error(f"Error in RiskAgent: {e}")
            return Command(goto=[], update={"messages": [AIMessage(content="Risk analysis failed. Please try again later.")]})