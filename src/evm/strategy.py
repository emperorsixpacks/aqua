from types.strategy import GeneratedStrategy, Step
from eth_account import Account
import os
from client import public_client, wallet_client
from src.config.addresses_config import STRATEGY
from src.evm.contracts.abis.strategy_abi import STRATEGY_ABI

async def create_strategy(strategy: GeneratedStrategy):
    if not os.getenv('PRIVATE_KEY'):
        raise ValueError("PRIVATE_KEY environment variable is required")
    
    account = Account.from_key(os.getenv('PRIVATE_KEY'))
    
    try:
        strategy_contract = wallet_client.eth.contract(
            address=STRATEGY,
            abi=STRATEGY_ABI["abi"]
        )
        transaction = strategy_contract.functions.createStrategy(
            strategy["name"],
            strategy["description"],
            [
                {
                    "connector": step["connector"],
                    "actionType": step["actionType"],
                    "assetsIn": step["assetsIn"],
                    "assetOut": step["assetOut"],
                    "amountRatio": step["amountRatio"],
                    "data": step["data"]
                }
                for step in strategy["steps"]
            ],
            strategy["minDeposit"]
        ).build_transaction({
            'from': account.address,
            'nonce': wallet_client.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': wallet_client.eth.gas_price
        })

        signed_txn = wallet_client.eth.account.sign_transaction(
            transaction, 
            private_key=os.getenv('PRIVATE_KEY')
        )

        tx_hash = wallet_client.eth.send_raw_transaction(signed_txn.rawTransaction)

        receipt = wallet_client.eth.wait_for_transaction_receipt(tx_hash)

        return receipt
    except Exception as error:
        print(f"Error creating strategy: {error}")
        raise