from .base_prompts import BasePrompt

class PerformanceAnalysisPrompt(BasePrompt):
    @classmethod
    def get_system_prompt(cls) -> str:
        return """You are a performance analyst expert. Your role is to:
        - Evaluate historical strategies based on performance data
        - Identify successful strategies and the factors contributing to their success
        - Identify failed strategies and provide insights into why they failed
        - Calculate success rates and summarize the overall performance
        - Provide actionable insights and recommendations for future strategies."""

    @classmethod
    def get_human_prompt(cls, performance_data: dict) -> str:
        return f"""Please analyze the following historical performance data and provide a summary:
        Performance Data: {performance_data}
        
        Please provide a detailed analysis including:
        1. Strategy Success Analysis
        2. Failure Analysis
        3. Success Rate Calculation
        4. Recommendations for Future Strategies"""