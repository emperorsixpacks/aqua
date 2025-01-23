import asyncio
import uuid
from app.graph import create_graph 

async def main():
    graph = create_graph()
    
    initial_state = {
        "messages": [],
        "market_data": {},
        "performance_metrics": {},
        "risk_assessment": {},
        "strategy": {},
        "asset": "USDC",
        "protocol": "moonwell",
    }
    
    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }
    
    async for chunk in graph.astream(
        initial_state, 
        config=config,
        stream_mode="values"
    ):
        if 'strategy_signals' in chunk:
            try:
                if isinstance(chunk['strategy_signals'], dict):
                    strategy = chunk['strategy_signals'].get('content')
                    if strategy:
                        print(strategy)
                else:
                    print(chunk['strategy_signals'])
            except Exception as e:
                print(f"Error processing chunk: {chunk}")

if __name__ == "__main__":
    asyncio.run(main())