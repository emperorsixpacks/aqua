from web3 import Web3
import os
import logging

logger = logging.getLogger("web3_client")

def create_web3_client():
    base_rpc_url = os.getenv('BASE_RPC_URL')
    if not base_rpc_url:
        raise ValueError("BASE_RPC_URL environment variable is required")

    provider = Web3.HTTPProvider(base_rpc_url)
    w3 = Web3(provider)
    
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to Ethereum node")
        
    return w3

try:
    web3_client = create_web3_client()
    public_client = web3_client
    wallet_client = web3_client  
except Exception as e:
    logger.error(f"Failed to initialize Web3 client: {e}", exc_info=True)
    raise