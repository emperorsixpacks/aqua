from .base_prompts import BasePrompt

class RiskAssessmentPrompt(BasePrompt):
    @classmethod
    def get_system_prompt(cls) -> str:
        return """You are a risk assessment expert. Your role is to:
        - Analyze market conditions and performance metrics
        - Calculate the overall risk level based on market trends and historical performance
        - Provide a risk assessment report, including actionable insights for managing risk."""

    @classmethod
    def get_human_prompt(cls, market_analysis: dict, performance_metrics: dict) -> str:
        return f"""Please assess the risk based on the following data:
        Market Analysis: {market_analysis}
        Performance Metrics: {performance_metrics}
        
        Provide a comprehensive risk assessment including:
        1. Overall Risk Level (Low, Medium, or High)
        2. Key Risk Factors
        3. Risk Mitigation Recommendations
        4. Actionable Insights"""