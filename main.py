from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from src.agents.market_agent import MarketAgent
from src.agents.risk_agent import RiskAgent
from src.agents.strategy_agent import StrategyAgent
from src.agents.performance_agent import PerformanceAgent
from states import AgentState

workflow = StateGraph(AgentState)   

market_agent = MarketAgent()
risk_agent = RiskAgent()
strategy_agent = StrategyAgent()
performance_agent = PerformanceAgent()

workflow.add_node("market_agent", market_agent.analyze_market)
workflow.add_node("risk_agent", risk_agent.assess_risk)
workflow.add_node("strategy_agent", strategy_agent.generate_strategy)
workflow.add_node("performance_agent", performance_agent.analyze_performance)

workflow.add_edge(START, "market_agent")
workflow.add_edge(START, "performance_agent")
workflow.add_edge("market_agent", "risk_agent")
workflow.add_edge("performance_agent", "risk_agent")
workflow.add_edge("risk_agent", "strategy_agent")
workflow.add_edge("strategy_agent", END)

graph = workflow.compile()



