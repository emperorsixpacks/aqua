import operator
from typing import Annotated, Any, List, Dict, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

def identity_reducer(current: Any, new: Any) -> Any:
    """Simple reducer that returns the new value."""
    return new

class AgentState(TypedDict):
    """State definition with reducers for all fields."""
    messages: Annotated[Sequence[BaseMessage], add_messages]  
    asset: Annotated[str, identity_reducer]
    protocol: Annotated[str, identity_reducer]
    market_analysis: Annotated[Dict, operator.ior]
    risk_analysis: Annotated[Dict, operator.ior]
    performance_metrics: Annotated[Dict, operator.ior]
    strategy_signals: Annotated[Dict, operator.ior]

