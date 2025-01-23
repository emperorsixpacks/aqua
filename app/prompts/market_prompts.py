from .base_prompts import BasePrompt

class MarketAnalysisPrompt(BasePrompt):
    @classmethod
    def get_system_prompt(cls) -> str:
        return """You are a financial analyst expert. Your role is to:
        - Identify key trends in market data
        - Assess overall market health based on supply, borrow rates, and liquidity
        - Provide a brief but thorough analysis of market conditions"""

    @classmethod
    def get_human_prompt(cls, market_data: dict) -> str:
        return f"""Please analyze the following market data:
        Market Data: {market_data}
        
        Provide a concise report covering:
        1. Market Trends
        2. Supply/Borrow Dynamics
        3. Liquidity Assessment
        4. Overall Market Health"""