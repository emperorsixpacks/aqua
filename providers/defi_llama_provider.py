import asyncio
import logging
from typing import List, Dict, Any, Tuple
from config.tokens_config import BASE_TOKENS
from providers.types.common import PriceChange, RiskMetrics, Token
from providers.types.market_types import CoinsResponse, Market, MarketData
from utils.api_client import fetch_with_retry

API_ENDPOINTS = {
    "DEFI_LLAMA": "https://api.llama.fi",
    "COINS_API": "https://coins.llama.fi",
    "YIELDS_API": "https://yields.llama.fi",
}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DEFI_LLAMA_PROVIDER")


async def fetch_token_prices_and_changes(tokens: List[str]) -> Tuple[CoinsResponse, Dict[str, PriceChange]]:
    token_ids = ",".join([f"base:{token}" for token in tokens])

    urls = {
        "prices": f"{API_ENDPOINTS['COINS_API']}/prices/current/{token_ids}",
        "day_changes": f"{API_ENDPOINTS['COINS_API']}/percentage/{token_ids}?period=24h",
        "week_changes": f"{API_ENDPOINTS['COINS_API']}/percentage/{token_ids}?period=7d",
        "month_changes": f"{API_ENDPOINTS['COINS_API']}/percentage/{token_ids}?period=30d",
    }

    try:
        prices, day_changes, week_changes, month_changes = await asyncio.gather(
            fetch_with_retry(urls["prices"]),
            fetch_with_retry(urls["day_changes"]),
            fetch_with_retry(urls["week_changes"]),
            fetch_with_retry(urls["month_changes"]),
        )

        changes: Dict[str, PriceChange] = {}
        for token in tokens:
            try:
                changes[token] = PriceChange(
                    day_24h=float(day_changes if isinstance(day_changes, (int, float)) 
                                else day_changes.get("coins", {}).get(f"base:{token}", {}).get("percentage", 0)),
                    week_7d=float(week_changes if isinstance(week_changes, (int, float))
                                else week_changes.get("coins", {}).get(f"base:{token}", {}).get("percentage", 0)),
                    month_30d=float(month_changes if isinstance(month_changes, (int, float))
                                  else month_changes.get("coins", {}).get(f"base:{token}", {}).get("percentage", 0))
                )
            except Exception as e:
                logger.error(f"Error processing changes for token {token}: {e}")
                changes[token] = PriceChange(day_24h=0, week_7d=0, month_30d=0)

        return prices, changes
    except Exception as e:
        logger.error(f"Error in fetch_token_prices_and_changes: {e}")
        return {}
async def fetch_defi_data() -> List[MarketData]:
    try:
        protocols = ["moonwell", "morpho"]
        tokens = list(BASE_TOKENS.values())

        protocol_tasks = [
            fetch_with_retry(f"{API_ENDPOINTS['DEFI_LLAMA']}/protocol/{protocol}")
            for protocol in protocols
        ]
        yield_pools_task = fetch_with_retry(f"{API_ENDPOINTS['YIELDS_API']}/pools")
        token_data_task = fetch_token_prices_and_changes(tokens)

        protocol_responses, yield_pools, (prices, changes) = await asyncio.gather(
            asyncio.gather(*protocol_tasks), yield_pools_task, token_data_task
        )

        base_yields = [
            pool for pool in yield_pools.get("data", [])
            if pool.get("chain") == "Base" and pool.get("project") in ["moonwell", "morpho"]
        ]

        moonwell_markets: Dict[str, Market] = {}
        for pool in base_yields:
            if pool.get("project") == "moonwell" and pool.get("underlyingTokens", [{}])[0] in BASE_TOKENS.values():
                token = pool["underlyingTokens"][0]
                protocol_data = protocol_responses[0]
                chain_tvls = protocol_data.get("currentChainTvls", {})

                base_tvl = chain_tvls.get("Base", 0) if isinstance(chain_tvls, dict) else 0
                base_borrowed = chain_tvls.get("Base-borrowed", 0) if isinstance(chain_tvls, dict) else 0
                
                apy_base = float(pool.get("apyBase", 0))
                apy = float(pool.get("apy", 0))
                
                moonwell_markets[token] = Market(
                    supplyRate=apy_base,
                    borrowRate=apy - apy_base,
                    totalSupply=float(base_tvl),
                    totalBorrow=float(base_borrowed),
                    liquidity=float(max(0, base_tvl - base_borrowed)),
                    collateralFactor=0.8,
                )

        tokens_data: Dict[str, Token] = {}
        prices_data = prices if isinstance(prices, dict) else {"coins": {}}
        
        for address in BASE_TOKENS.values():
            coin_key = f"base:{address}"
            coins_data = prices_data.get("coins", {})
            price_data = coins_data.get(coin_key, {})
            price_change = changes.get(address, PriceChange(0, 0, 0))
            
            tokens_data[address] = Token(
                price=float(price_data.get("price", 0)),
                priceChange=price_change,
                decimals=6 if address == BASE_TOKENS["USDC"] else 18,
                symbol=price_data.get("symbol", ""),
                totalSupply=0,
            )

        risk_metrics: Dict[str, RiskMetrics] = {
            address: RiskMetrics(
                tvlUSD=float(moonwell_markets[address].totalSupply if address in moonwell_markets else 0),
                volume24hUSD=0,
                uniqueUsers24h=0,
                healthFactor=0.85,
                lastUpdate=int(asyncio.get_running_loop().time()),
            )
            for address in tokens
        }

        return [
            MarketData(
                timestamp=int(asyncio.get_running_loop().time()),
                blockNumber=18000000,
                protocols={
                    "moonwell": {"markets": moonwell_markets},
                },
                tokens=tokens_data,
                riskMetrics=risk_metrics,
            )
        ]
    except Exception as e:
        logger.error(f"Error in fetch_defi_data: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise Exception(f"Error fetching DeFi data: {str(e)}")


async def get_market_data() -> List[MarketData]:
    try:
        return await fetch_defi_data()
    except Exception as e:
        logger.error(f"Failed to fetch market data: {str(e)}")
        return []