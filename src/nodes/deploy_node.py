import json
import logging
from src.services.performance_service import PerformanceService
from src.jobs.strategy_job import schedule_strategy_deployment
from langchain_core.messages import AIMessage

logger = logging.getLogger("deploy_node")


async def deploy(state: dict) -> dict:
    try:
        strategy_response = state.get("strategy_signals", {})
        if not strategy_response:
            raise ValueError("No strategy available for deployment.")

        strategy_content = json.loads(strategy_response.get("content", "{}"))
        await PerformanceService.save_strategy(strategy_content)
        await schedule_strategy_deployment(strategy_content)

        state["messages"] = state.get("messages", []) + [
            AIMessage(content="Strategy successfully deployed."),
            AIMessage(content=f"Deployed strategy: {json.dumps(strategy_content, indent=2)}")
        ]
        
        state["deployment_status"] = "success"

        return state

    except Exception as e:
        logger.error(f"Error during strategy deployment: {e}", exc_info=True)
        state["messages"] = state.get("messages", []) + [
            AIMessage(content="Error during strategy deployment. Please try again later.")
        ]
        state["deployment_status"] = "error"

        return state
