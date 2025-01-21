import logging
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.conditions.strategy_condition import add_strategy_conditional_edges
from src.nodes.deploy_node import deploy
from src.nodes.reviewer_node import reviewer
from src.nodes.market_node import analyze_market
from src.nodes.risk_node import assess_risk
from src.nodes.strategy_node import generate_strategy
from src.nodes.performance_node import analyze_performance
from src.states import AgentState
from langgraph.types import Command, interrupt

logger = logging.getLogger("Graph")
logging.basicConfig(level=logging.INFO)

def error_handler(state: AgentState):
    print("An error occurred in the workflow.")
    return state

memory = MemorySaver()
workflow = StateGraph(AgentState)

workflow.add_node("analyze_market", analyze_market)
workflow.add_node("analyze_performance", analyze_performance)
workflow.add_node("assess_risk", assess_risk)
workflow.add_node("generate_strategy", generate_strategy)
workflow.add_node("reviewer", reviewer)
workflow.add_node("deploy", deploy)
workflow.add_node("error_handler", error_handler)

workflow.add_edge(START, "analyze_market")
workflow.add_edge(START, "analyze_performance")
workflow.add_edge("analyze_market", "assess_risk")
workflow.add_edge("analyze_performance", "assess_risk")
workflow.add_edge("assess_risk", "generate_strategy")
workflow.add_edge("generate_strategy", "reviewer")
add_strategy_conditional_edges(
    workflow,
    from_node="reviewer",
    approve_node="deploy",
    refine_node="generate_strategy"
)
workflow.add_edge("deploy", END)
workflow.add_edge("error_handler", END)

graph = workflow.compile(checkpointer=memory)

def create_graph():
    return graph
