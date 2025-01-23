from dataclasses import dataclass

@dataclass
class RiskMetrics:
    tvlUSD: float
    volume24hUSD: float
    uniqueUsers24h: int
    healthFactor: float
    lastUpdate: int

@dataclass
class PriceChange:
    day_24h: float
    week_7d: float
    month_30d: float

@dataclass
class Token:
    price: float
    priceChange: PriceChange
    decimals: int
    symbol: str
    totalSupply: int
