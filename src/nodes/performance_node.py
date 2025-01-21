import logging
from src.config.llm_config import CREATIVE_TEMPERATURE, DEFAULT_TEMPERATURE, GPT3_5_MODEL
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.prompts.performance_prompts import PerformanceAnalysisPrompt
from src.services.performance_service import PerformanceService

logger = logging.getLogger("performance_node")

async def analyze_performance(state: dict) -> dict:
    try:
        performance_data =await PerformanceService.get_latest_performance_data()

        logger.info(f"Fetched historical performance data successfully: {performance_data}")

        model = ChatOpenAI(
            model=GPT3_5_MODEL
        )
        
        messages = [
            SystemMessage(content=PerformanceAnalysisPrompt.get_system_prompt()),
            HumanMessage(content=PerformanceAnalysisPrompt.get_human_prompt(
                performance_data=performance_data
            ))
        ]

        analysis_response = await model.ainvoke(messages)
        logger.info(f"Performance analysis completed: {analysis_response}")

        state["messages"] = state.get("messages", []) + [AIMessage(content=f"Performance analysis report: {analysis_response}")]
        state["performance_metrics"] = analysis_response
        return state
    
    except Exception as e:
        logger.error(f"Error analyzing performance: {e}", exc_info=True)
        state["messages"] = state.get("messages", []) + [AIMessage(content="An error occurred while analyzing performance. Please try again later.")]

    
