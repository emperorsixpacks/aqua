import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

logger = logging.getLogger("risk_node")

async def assess_risk(state: dict) -> dict:
    try:
        market_analysis = state.get("market_analysis", {})
        performance_metrics = state.get("performance_metrics", {})

        logger.info(f"Received market analysis and performance metrics: {market_analysis}, {performance_metrics}")

        model = ChatOpenAI(model="gpt-3.5-turbo")
        system_instructions = SystemMessage(content="""You are a risk assessment expert. Your role is to:
        - Analyze market conditions and performance metrics
        - Calculate the overall risk level based on market trends and historical performance
        - Provide a risk assessment report, including actionable insights for managing risk.""")

        messages = [
            system_instructions,
            HumanMessage(content=f"""Please assess the risk based on the following data:
            Market Analysis: {market_analysis}
            Performance Metrics: {performance_metrics}
            Provide a risk level of Low, Medium, or High based on the analysis.""")
        ]

        analysis_response = await model.ainvoke(messages)
        logger.info(f"Risk analysis completed: {analysis_response}")

        state["messages"] = state.get("messages", []) + [AIMessage(content=f"Risk analysis report: {analysis_response}")]
        state["risk_analysis"] = {"level": analysis_response}
        return state
    
    except Exception as e:
        logger.error(f"Error assessing risk: {e}", exc_info=True)
        state["messages"] = state.get("messages", []) + [AIMessage(content="Risk analysis failed. Please try again later.")]


