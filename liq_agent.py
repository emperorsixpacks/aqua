from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.nodes.market_node import analyze_market
from src.nodes.risk_node import assess_risk
from src.nodes.strategy_node import generate_strategy
from src.nodes.performance_node import analyze_performance
from states import AgentState

memory = MemorySaver()

workflow = StateGraph(AgentState)

workflow.add_node("analyze_market", analyze_market)
workflow.add_node("analyze_performance", analyze_performance)
workflow.add_node("assess_risk", assess_risk)
workflow.add_node("generate_strategy", generate_strategy)

workflow.add_edge(START, "analyze_market")
workflow.add_edge(START, "analyze_performance")
workflow.add_edge("analyze_market", "assess_risk")
workflow.add_edge("analyze_performance", "assess_risk")
workflow.add_edge("assess_risk", "generate_strategy")
workflow.add_edge("generate_strategy", END)

graph = workflow.compile(checkpointer=memory)
