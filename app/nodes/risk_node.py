import logging
from app.config.llm_config import CREATIVE_TEMPERATURE, DEFAULT_TEMPERATURE, GPT3_5_MODEL
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.prompts.risk_prompts import RiskAssessmentPrompt

logger = logging.getLogger("risk_node")

async def assess_risk(state: dict) -> dict:
    try:
        market_analysis = state.get("market_analysis", {})
        performance_metrics = state.get("performance_metrics", {})

        logger.info(f"Received market analysis and performance metrics: {market_analysis}, {performance_metrics}")

        model = ChatOpenAI(
            model=GPT3_5_MODEL
        )
        
        messages = [
            SystemMessage(content=RiskAssessmentPrompt.get_system_prompt()),
            HumanMessage(content=RiskAssessmentPrompt.get_human_prompt(
                market_analysis=market_analysis,
                performance_metrics=performance_metrics
            ))
        ]

        analysis_response = await model.ainvoke(messages)
        logger.info(f"Risk analysis completed: {analysis_response}")

        state["messages"] = state.get("messages", []) + [AIMessage(content=f"Risk analysis report: {analysis_response}")]
        state["risk_analysis"] = {"level": analysis_response}
        return state
    
    except Exception as e:
        logger.error(f"Error assessing risk: {e}", exc_info=True)
        state["messages"] = state.get("messages", []) + [AIMessage(content="Risk analysis failed. Please try again later.")]


