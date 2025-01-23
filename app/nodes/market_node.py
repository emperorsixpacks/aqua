import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.prompts.market_prompts import MarketAnalysisPrompt
from app.services.market_service import MarketService
from app.config.llm_config import CREATIVE_TEMPERATURE, GPT3_5_MODEL, DEFAULT_TEMPERATURE

logger = logging.getLogger("market_node")

async def analyze_market(state: dict) -> dict:
    try:
        market_data = await MarketService.get_latest_market_data()
        logger.info(f"Fetched market data successfully: {market_data}")

        model = ChatOpenAI(
            model=GPT3_5_MODEL,
        )

        messages = [
            SystemMessage(content=MarketAnalysisPrompt.get_system_prompt()),
            HumanMessage(content=MarketAnalysisPrompt.get_human_prompt(market_data=market_data))
        ]

        analysis_response = await model.ainvoke(messages)
        logger.info(f"Market analysis generated: {analysis_response}")

        state["messages"] = state.get("messages", []) + [AIMessage(content=f"Market analysis report: {analysis_response}")]
        state["market_analysis"] = analysis_response
        return state
    
    except Exception as e:
        logger.error(f"Error during market analysis: {e}", exc_info=True)
        state["messages"] = state.get("messages", []) + [AIMessage(content="Error analyzing market data. Please try again later.")]

   
