from web3 import Web3
from eth_account import Account
import os

if not os.getenv('PRIVATE_KEY'):
    raise ValueError("PRIVATE_KEY environment variable is required")

account = Account.from_key(os.getenv('PRIVATE_KEY'))

base_rpc_url = os.getenv('BASE_RPC_URL')
w3 = Web3(Web3.HTTPProvider(base_rpc_url))

public_client = w3
wallet_client = w3  