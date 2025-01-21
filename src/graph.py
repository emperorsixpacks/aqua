from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.nodes.deploy_node import deploy
from src.nodes.reviewer_node import reviewer
from src.nodes.market_node import analyze_market
from src.nodes.risk_node import assess_risk
from src.nodes.strategy_node import generate_strategy
from src.nodes.performance_node import analyze_performance
from src.states import AgentState

def reviewer_routing(state: AgentState):
    feedback = state.get("review_feedback", "").lower()
    print(f"Reviewer feedback: {feedback}")
    if "refine" in feedback:
        return "generate_strategy"
    elif "approve" in feedback:
        return "deploy"
    return "reviewer"


memory = MemorySaver()
workflow = StateGraph(AgentState)

workflow.add_node("analyze_market", analyze_market)
workflow.add_node("analyze_performance", analyze_performance)
workflow.add_node("assess_risk", assess_risk)
workflow.add_node("generate_strategy", generate_strategy)
workflow.add_node("reviewer", reviewer)
workflow.add_node("deploy", deploy)

workflow.add_edge(START, "analyze_market")
workflow.add_edge(START, "analyze_performance")
workflow.add_edge("analyze_market", "assess_risk")
workflow.add_edge("analyze_performance", "assess_risk")
workflow.add_edge("assess_risk", "generate_strategy")
workflow.add_edge("generate_strategy", "reviewer")
workflow.add_conditional_edges("reviewer", reviewer_routing)
workflow.add_edge("deploy", END)

graph = workflow.compile(checkpointer=memory)

def create_graph():
    return graph     