from langgraph.types import Command
from langchain_core.messages import AIMessage
from services.performance_service import PerformanceService
import logging
from typing import Dict

logger = logging.getLogger("PerformanceAgent")
logger.setLevel(logging.INFO)

class PerformanceAgent:
    async def analyze_performance(self, state: Dict) -> Command:
        """Performance analysis agent that evaluates historical strategies."""
        try:
            performance_data = PerformanceService.fetch_historical_performance()
            logger.info("Fetched historical performance data successfully.")

            performance_summary = self._analyze_data(performance_data)
            logger.info(f"Performance analysis completed: {performance_summary}")

            messages = state.get("messages", [])
            messages.append(AIMessage(content=f"Performance analysis: {performance_summary}"))

            return Command(goto=[], update={"messages": messages, "performance_metrics": performance_summary})
        except Exception as e:
            logger.error(f"Error in PerformanceAgent: {e}")
            return Command(goto=[], update={"messages": [AIMessage(content="Performance analysis failed.")]})


    def _analyze_data(self, performance_data: Dict) -> Dict:
        """Analyze the performance data and generate insights."""

        successful_strategies = [
            strategy for strategy, outcome in performance_data.items() if outcome == "success"
        ]
        failed_strategies = [
            strategy for strategy, outcome in performance_data.items() if outcome == "failure"
        ]

        performance_summary = {
            "total_strategies": len(performance_data),
            "successful_strategies": len(successful_strategies),
            "failed_strategies": len(failed_strategies),
            "success_rate": f"{(len(successful_strategies) / len(performance_data)) * 100:.2f}%" if performance_data else "N/A"
        }
        return performance_summary
