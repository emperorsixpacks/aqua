from .base_prompts import BasePrompt

class StrategyGenerationPrompt(BasePrompt):
    @classmethod
    def get_system_prompt(cls) -> str:
        return """You are a DeFi strategy analyst. Your task is to generate or analyze a DeFi strategy based on the following actions:

        - SUPPLY: The user supplies an asset (e.g., USDC, WETH) and receives wrapped tokens (e.g., mUSDC, mWETH) in return. The user earns interest on the supplied asset, paid in the same asset.
        - WITHDRAW: The user withdraws wrapped tokens and receives the original asset (e.g., USDC, WETH) back.
        - BORROW: The user borrows an asset (e.g., USDC, WETH) by providing collateral (e.g., mUSDC, mWETH). The amount borrowed is determined by the loan-to-value (LTV) ratio.
        - REPAY: The user repays the borrowed asset along with any interest, using the same asset they borrowed (e.g., repay USDC for borrowed USDC).

        You can generate or analyze a DeFi strategy based on these actions and provide a clear, actionable strategy."""

    @classmethod
    def get_human_prompt(cls, risk_analysis: dict, asset: str, protocol: str, 
                        protocol_config: dict, strategy_config: dict,
                        base_token_address: str, min_deposit: str,
                        market_addresses: dict, connector: str) -> str:
        market_address_text = ",\n  ".join([f"{key}: {value}" for key, value in market_addresses.items()])
        
        return f"""Generate a one step strategy for the given asset and protocol:
        - Risk Analysis: {risk_analysis}
        - Asset: {asset}
        - Protocol: {protocol.capitalize()}
        - Connector: {connector}
        - Market Token Address(SUPPLY receives, WITHDRAW sends - mToken address): 
        {market_address_text}
        - Base Token Address(SUPPLY sends, WITHDRAW receives, BORROW receives, REPAY sends): 
        {base_token_address}
        - Minimum Deposit: {min_deposit}
        - Supported Actions: {', '.join(protocol_config.get('supportedActions', []))}
        - Constraints: {strategy_config.get('constraints', {})}

        Format the strategy as a valid JSON object:
        {{
            "name": "Strategy name",
            "description": "Detailed explanation about the strategy",
            "steps": [
                {{
                    "connector": "{connector}",
                    "actionType": "SUPPLY/BORROW/WITHDRAW/REPAY",
                    "assetsIn": ["0xAddress"],
                    "assetOut": "0xAddress",
                    "amountRatio": "10000",
                    "data": "0x"
                }}
            ],
            "minDeposit": "{min_deposit}"
        }}"""