import os
from typing import Dict, Any
from web3 import Web3
from eth_account import Account
from eth_typing import Address
from app.evm.client import public_client, wallet_client
from app.evm.contracts.abis.strategy_abi import STRATEGY_ABI
from app.types.strategy import ACTION_TYPES

async def deploy_strategy_onchain(
   strategy: Dict[str, Any],
   contract_address: Address,
   contract_abi: Dict[str, Any] = STRATEGY_ABI
) -> Dict[str, Any]:
   private_key = os.getenv('PRIVATE_KEY')
   if not private_key:
       raise ValueError("PRIVATE_KEY environment variable is required")

   account = Account.from_key(private_key)
   
   strategy_contract = public_client.eth.contract(
       address=contract_address,
       abi=contract_abi["abi"]
   )

   formatted_steps = [
       (
           Web3.to_checksum_address(step["connector"]),
           ACTION_TYPES[step["actionType"]],
           [Web3.to_checksum_address(addr) for addr in step["assetsIn"]],
           Web3.to_checksum_address(step["assetOut"]),
           int(step["amountRatio"]),
           Web3.to_bytes(hexstr=step["data"]) if step["data"] else b''
       )
       for step in strategy["steps"]
   ]

   transaction = strategy_contract.functions.createStrategy(
       strategy["name"],
       strategy["description"],
       formatted_steps,
       int(strategy["minDeposit"])
   ).build_transaction({
       'from': account.address,
       'nonce': public_client.eth.get_transaction_count(account.address),
       'gas': 2000000,
       'maxFeePerGas': public_client.eth.max_priority_fee * 2 + public_client.eth.gas_price,
       'maxPriorityFeePerGas': public_client.eth.max_priority_fee
   })

   signed_txn = wallet_client.eth.account.sign_transaction(
       transaction,
       private_key=private_key
   )
   tx_hash = wallet_client.eth.send_raw_transaction(signed_txn.raw_transaction)
   
   return wallet_client.eth.wait_for_transaction_receipt(tx_hash)