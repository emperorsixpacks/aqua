import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.services.performance_service import PerformanceService

logger = logging.getLogger("performance_node")

async def analyze_performance(state: dict) -> dict:
    try:
        performance_data = PerformanceService.get_latest_performance_data()

        logger.info(f"Fetched historical performance data successfully: {performance_data}")

        model = ChatOpenAI(model="gpt-3.5-turbo")
        system_instructions = SystemMessage(content="""You are a performance analyst expert. Your role is to:
        - Evaluate historical strategies based on performance data
        - Identify successful strategies and the factors contributing to their success
        - Identify failed strategies and provide insights into why they failed
        - Calculate success rates and summarize the overall performance
        - Provide actionable insights and recommendations for future strategies.""")

        messages = [
            system_instructions,
            HumanMessage(content=f"""Please analyze the following historical performance data and provide a summary:
            Performance Data: {performance_data}
            Please identify successful strategies, failed strategies, and calculate the success rate. Also, provide recommendations for improving future strategies.""")
        ]

        analysis_response = await model.ainvoke(messages)
        logger.info(f"Performance analysis completed: {analysis_response}")

        state["messages"] = state.get("messages", []) + [AIMessage(content=f"Performance analysis report: {analysis_response}")]
        state["performance_metrics"] = analysis_response
        return state
    
    except Exception as e:
        logger.error(f"Error analyzing performance: {e}", exc_info=True)
        state["messages"] = state.get("messages", []) + [AIMessage(content="An error occurred while analyzing performance. Please try again later.")]

    
