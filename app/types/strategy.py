from typing import List, TypedDict, Union
from eth_typing import Address, HexStr

class Step(TypedDict):
    connector: Address
    actionType: int
    assetsIn: List[Address]
    assetOut: Address
    amountRatio: int
    data: HexStr

class GeneratedStrategy(TypedDict):
    name: str
    description: str
    steps: List[Step]
    minDeposit: int


ACTION_TYPES = {
   'SUPPLY': 0,
   'BORROW': 1, 
   'WITHDRAW': 2,
   'REPAY': 3,
}