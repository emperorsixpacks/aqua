from langchain_core.messages import AIMessage
from langgraph.types import Command
from typing import Dict
import logging

logger = logging.getLogger("RiskAgent")
logger.setLevel(logging.INFO)

class RiskAgent:
    async def assess_risk(self, state: Dict) -> Command:
        """Risk assessment agent that evaluates risks based on market and performance data."""
        try:
            messages = state.get("messages", [])
            market_analysis = state.get("market_analysis", {})
            performance_metrics = state.get("performance_metrics", {})

            risk_level = self._calculate_risk(market_analysis, performance_metrics)
            risk_message = f"Risk analysis completed. Risk level: {risk_level}."

            logger.info(risk_message)
            messages.append(AIMessage(content=risk_message))
            return Command(goto="strategy_agent", update={"messages": messages, "risk_analysis": {"level": risk_level}})
        except Exception as e:
            logger.error(f"Error in RiskAgent: {e}")
            return Command(goto=[], update={"messages": [AIMessage(content="Risk analysis failed.")]})


    def _calculate_risk(self, market_analysis: Dict, performance_metrics: Dict) -> str:
        """
        Calculate the risk level based on market analysis and performance metrics.

        Risk levels:
        - Low: Market conditions are favorable and historical strategies have high success rates.
        - Medium: Mixed market conditions or moderate historical performance.
        - High: Unfavorable market conditions or poor historical performance.
        """
    
        if not market_analysis or not performance_metrics:
            return "High" 

        success_rate = performance_metrics.get("success_rate", "0%").strip("%")
        success_rate = float(success_rate) if success_rate else 0.0

        market_condition = "bullish" if "bullish" in market_analysis else "neutral"
        if "bearish" in market_analysis:
            market_condition = "bearish"

        if success_rate > 70 and market_condition == "bullish":
            return "Low"
        elif 50 <= success_rate <= 70 or market_condition == "neutral":
            return "Medium"
        else:
            return "High"
