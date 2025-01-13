from langchain_openai import ChatOpenAI
from langgraph.types import Command
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langgraph.graph import END
from typing import Dict
import logging
from src.services.market_service import MarketService


logger = logging.getLogger("MarketAgent")
logger.setLevel(logging.INFO)

class MarketAgent:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
        self.system_instructions = SystemMessage(content="""You are a financial analyst expert. Your role is to:
        - Identify key trends in market data
        - Assess overall market health based on supply, borrow rates, and liquidity
        - Determine if the market is bullish, bearish, or neutral
        - Provide a brief but thorough analysis of market conditions""")

    async def analyze_market(self, state: Dict) -> Command:
        try:
            market_data =  MarketService.get_latest_market_data()
            logger.info("Fetched market data successfully.", {market_data})

            messages = [
                self.system_instructions,
                HumanMessage(
                    content=f"""Please analyze the following market data:
                    Market Data: {market_data}
                    Please analyze the data and give a concise report based on the instructions provided."""
                )
            ]

            analysis_response = await self.model.ainvoke(messages)
            logger.info(f"Market analysis generated: {analysis_response}")

            messages = state.get("messages", [])
            messages.append(AIMessage(content=f"Market analysis report: {analysis_response}"))

            return Command(goto=[], update={"messages": messages, "market_analysis": analysis_response})

        except Exception as e:
            logger.error(f"Error during market analysis: {e}")
            return Command(goto=END, update={"messages": [AIMessage(content="Error analyzing market data. Please try again later.")]})
