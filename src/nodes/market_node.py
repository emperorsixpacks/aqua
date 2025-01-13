import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.services.market_service import MarketService

logger = logging.getLogger("market_node")

async def analyze_market(state: dict) -> dict:
    try:
        market_data = MarketService.get_latest_market_data()
        logger.info(f"Fetched market data successfully: {market_data}")

        model = ChatOpenAI(model="gpt-3.5-turbo")
        system_instructions = SystemMessage(content="""You are a financial analyst expert. Your role is to:
        - Identify key trends in market data
        - Assess overall market health based on supply, borrow rates, and liquidity
        - Provide a brief but thorough analysis of market conditions""")

        messages = [
            system_instructions,
            HumanMessage(
                content=f"""Please analyze the following market data:
                Market Data: {market_data}
                Provide a concise report based on the instructions."""
            )
        ]

        analysis_response = await model.ainvoke(messages)
        logger.info(f"Market analysis generated: {analysis_response}")

        state["messages"] = state.get("messages", []) + [AIMessage(content=f"Market analysis report: {analysis_response}")]
        state["market_analysis"] = analysis_response
        return state
    
    except Exception as e:
        logger.error(f"Error during market analysis: {e}", exc_info=True)
        state["messages"] = state.get("messages", []) + [AIMessage(content="Error analyzing market data. Please try again later.")]

   
