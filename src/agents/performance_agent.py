from langchain_openai import ChatOpenAI
from langgraph.types import Command
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from src.services.performance_service import PerformanceService
import logging
from typing import Dict

logger = logging.getLogger("PerformanceAgent")
logger.setLevel(logging.INFO)

class PerformanceAgent:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
        self.system_instructions = SystemMessage(content="""You are a performance analyst expert. Your role is to:
        - Evaluate historical strategies based on performance data
        - Identify successful strategies and the factors contributing to their success
        - Identify failed strategies and provide insights into why they failed
        - Calculate success rates and summarize the overall performance
        - Provide actionable insights and recommendations for future strategies.""")

    async def analyze_performance(self, state: Dict) -> Command:
        try:
            performance_data = PerformanceService.get_latest_performance_data()

            logger.info(f"Fetched historical performance data successfully: {performance_data}")

            messages = [
                self.system_instructions,
                HumanMessage(content=f"""Please analyze the following historical performance data and provide a summary:
                Performance Data: {performance_data}
                Please identify successful strategies, failed strategies, and calculate the success rate. Also, provide recommendations for improving future strategies.""")
            ]

            analysis_response = await self.model.ainvoke(messages)
            logger.info(f"Performance analysis completed: {analysis_response}")

            messages = state.get("messages", [])
            messages.append(AIMessage(content=f"Performance analysis report: {analysis_response}"))

            return Command(goto=[], update={"messages": messages, "performance_metrics": analysis_response})

        except Exception as e:
            logger.error(f"Error in PerformanceAgent: {e}")
            return Command(goto=[], update={"messages": [AIMessage(content="An error occurred while analyzing performance. Please try again later.")]})

