from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class Market:
    supplyRate: float
    borrowRate: float
    totalSupply: int
    totalBorrow: int
    liquidity: int
    collateralFactor: float

@dataclass
class Vault:
    apy: float
    tvl: int
    token: str
    performanceFee: float
    timelock: int

@dataclass
class MarketData:
    timestamp: int
    blockNumber: int
    protocols: Dict[str, Dict[str, Dict[str, Market]]]
    tokens: Dict[str, "Token"]
    riskMetrics: Dict[str, "RiskMetrics"]

@dataclass
class CoinsResponse:
   coins: Dict[
        str,
        Dict[
            str,
            Optional[float],  
        ]
    ]