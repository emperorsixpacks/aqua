from langchain_openai import ChatOpenAI
from langgraph.types import Command
from langchain_core.messages import AIMessage
from langgraph.graph import END
from typing import Dict
import logging
from services.market_service import MarketService

logger = logging.getLogger("MarketAgent")
logger.setLevel(logging.INFO)
class MarketAgent:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-3.5-turbo")

    async def analyze_market(self, state: Dict) -> Command:
        try:
            market_data = MarketService.get_latest_market_data()
            logger.info("Fetched market data successfully.",{market_data})

            instructions = """
            You are a financial analyst. I will provide you with market data. Please analyze the data and provide a report.
            - Identify key trends in the data.
            - Assess the overall health of the market based on supply, borrow rates, and liquidity.
            - Determine if the market is bullish, bearish, or neutral.
            - Provide a brief analysis of the market conditions.
            """

            market_insight_prompt = f"""
            {instructions}
            
            Here is the market data:
            {market_data}
            
            Please analyze the data and give a concise report based on the instructions provided.
            """

            analysis_response = await self.model.ainvoke(market_insight_prompt)
            logger.info(f"Market analysis generated: {analysis_response}")

            messages = state.get("messages", [])
            messages.append(AIMessage(content=f"Market analysis: {analysis_response}"))

            return Command(goto=[], update={"messages": messages, "market_analysis": analysis_response})

        except Exception as e:
            logger.error(f"Error during market analysis: {e}")
            return Command(goto=END, update={"messages": [AIMessage(content="Error analyzing market data. Please try again later.")]})
