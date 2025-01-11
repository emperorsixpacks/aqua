from typing import List, Optional
from dataclasses import dataclass

@dataclass
class LlamaPredictions:
    predictedClass: Optional[str]
    predictedProbability: Optional[float]
    binnedConfidence: Optional[float]

@dataclass
class LlamaPool:
    chain: str
    project: str
    symbol: str
    tvlUsd: float
    apyBase: float
    apyReward: Optional[float]
    apy: float
    rewardTokens: Optional[List[str]]
    pool: str
    apyPct1D: Optional[float]
    apyPct7D: Optional[float]
    apyPct30D: Optional[float]
    stablecoin: bool
    ilRisk: str
    exposure: str
    predictions: LlamaPredictions
    poolMeta: Optional[str]
    mu: float
    sigma: float
    count: int
    outlier: bool
    underlyingTokens: List[str]
    il7d: Optional[float]
    apyBase7d: Optional[float]
    apyMean30d: Optional[float]
    volumeUsd1d: Optional[float]
    volumeUsd7d: Optional[float]
    apyBaseInception: Optional[float]

@dataclass
class LlamaYieldResponse:
    status: str
    data: List[LlamaPool]

@dataclass
class LlamaProtocolResponse:
    id: str
    name: str
    url: str
    description: str
    logo: str
    chains: List[str]
    gecko_id: str
    cmcId: str
    treasury: Optional[str]
    twitter: Optional[str]
    governanceID: Optional[List[str]]
    currentChainTvls: dict
    chainTvls: dict
