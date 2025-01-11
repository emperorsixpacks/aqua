import operator
from typing import Annotated, List, Dict, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]  
    market_analysis: dict
    risk_analysis: dict
    performance_metrics: dict
    strategy_signals: dict
    asset: str = "" 
    protocol: str = "" 