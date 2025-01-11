import json
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langgraph.graph import END
from typing import Dict
import logging

from config.min_deposits import MIN_DEPOSITS
from config.protocols_config import PROTOCOLS_CONFIG
from config.strategy_config import STRATEGY_CONFIG
from config.tokens_config import BASE_TOKENS
from evm.addresses import CONNECTORS

logger = logging.getLogger("StrategyAgent")
logger.setLevel(logging.INFO)

class StrategyAgent:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
        self.system_instructions = SystemMessage(content="""You are a DeFi strategy analyst. Your task is to generate or analyze a DeFi strategy based on the following actions:

        - SUPPLY: The user supplies an asset (e.g., USDC, WETH) and receives wrapped tokens (e.g., mUSDC, mWETH) in return. The user earns interest on the supplied asset, paid in the same asset.
        - WITHDRAW: The user withdraws wrapped tokens and receives the original asset (e.g., USDC, WETH) back.
        - BORROW: The user borrows an asset (e.g., USDC, WETH) by providing collateral (e.g., mUSDC, mWETH). The amount borrowed is determined by the loan-to-value (LTV) ratio.
        - REPAY: The user repays the borrowed asset along with any interest, using the same asset they borrowed (e.g., repay USDC for borrowed USDC).

        You can generate or analyze a DeFi strategy based on these actions and provide a clear, actionable strategy.""")

    async def generate_strategy(self, state: Dict) -> Command:
        try:
            messages = state.get("messages", [])
            messages.append(self.system_instructions)
            risk_analysis = state.get("risk_analysis", "")
            asset = state.get("asset")
            protocol = state.get("protocol")
            protocol_config = PROTOCOLS_CONFIG[protocol]
            strategy_config = STRATEGY_CONFIG.get(asset.lower(), {})
            base_token_address = BASE_TOKENS[asset]
            min_deposit = MIN_DEPOSITS.get(asset, "0")

            markets = protocol_config["addresses"]["markets"]
            market_address_text = ",\n  ".join([f"{key}: {value}" for key, value in markets.items()])
            human_message = HumanMessage(content=f"""Generate a one step strategy for the given asset and protocol:
            - Risk Analysis: {risk_analysis}
            - Asset: {asset}
            - Protocol: {protocol.capitalize()}
            - Connector: {CONNECTORS[protocol]}
            - Market Token Address(SUPPLY receives, WITHDRAW sends - mToken address like mWETH, mUSDC, mBTC, mcBTC): 
            {market_address_text}
            - Base Token Address(SUPPLY sends, WITHDRAW receives, BORROW receives, REPAY sends - Base token address like WETH, USDC, BTC, cBTC): 
            {base_token_address}
            - Minimum Deposit: {min_deposit}
            - Supported Actions: {', '.join(protocol_config['supportedActions'])}
            - Constraints: {json.dumps(strategy_config.get('constraints', {}), indent=2)}

            Instructions for generating the strategy:
            - Determine the appropriate `actionType` based on the protocol's supported actions.
            - Dynamically decide the `assetsIn` and `assetOut` fields based on the asset, protocol, and market provided.
            - Use `assetsIn` for the input asset (e.g., for SUPPLY or REPAY).
            - Use `assetOut` for the output asset (e.g., for BORROW or WITHDRAW).
            - Select appropriate values for `assetsIn` and `assetOut` from the given `Market Addresses` or fallback to the `Base Token Address`.
            - Adhere to any provided constraints.

            Format the strategy as a valid JSON object:
            {{
                "name": "Strategy name",
                "description": "Detailed explanation about the strategy",
                "steps": [
                    {{
                        "connector": "{CONNECTORS[protocol]}",
                        "actionType": "SUPPLY/BORROW/WITHDRAW/REPAY",
                        "assetsIn": ["0xAddress"],
                        "assetOut": "0xAddress",
                        "amountRatio": "10000",
                        "data": "0x"
                    }}
                ],
                "minDeposit": "{min_deposit}"
            }}
            Ensure the JSON is properly formatted without comments.            

            """)

            messages.append(human_message)

            strategy_response = await self.model.ainvoke(messages)
            logger.info(f"DeFi strategy generated: {strategy_response}")

            messages.append(AIMessage(content=f"Generated DeFi strategy: {strategy_response}"))

            return Command(goto=END, update={"messages": messages, "strategy_signals": strategy_response})

        except Exception as e:
            logger.error(f"Error during strategy generation: {e}")
            return Command(goto=END, update={"messages": [AIMessage(content="Error generating DeFi strategy. Please try again later.")]})
