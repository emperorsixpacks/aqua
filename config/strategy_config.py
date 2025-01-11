STRATEGY_CONFIG = {
    "usdc": {
        "steps": 1,
        "maxProtocols": 3,
        "minYield": 4.0,  
        "maxRiskScore": 7,  
        "supportedProtocols": ["moonwell"],
        "constraints": {
            "minLendingRatio": 0.8, 
            "minStablecoinExposure": 0.95,  
            "supportedStables": [
                "0x833589fCD6E08f4c7C32D4f71b54bdA02913",  
            ],
        },
    },
    "weth": {
        "steps": 1,
        "maxProtocols": 3,
        "minYield": 3.0, 
        "maxRiskScore": 8,
        "supportedProtocols": ["moonwell"],
        "constraints": {
            "minLendingRatio": 0.6,  
            "supportedTokens": [
                "0x4200000000000000000000000000000000000006",  
            ],
        },
    },
}
