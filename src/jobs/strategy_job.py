from datetime import datetime
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.evm.strategy import deploy_strategy_onchain
from src.config.addresses_config import STRATEGY_ADDRESS
import asyncio

logger = logging.getLogger("strategy_job")
scheduler = AsyncIOScheduler()

async def strategy_deployment_job(strategy: dict):
    try:
        receipt = await deploy_strategy_onchain(
            strategy=strategy,
            contract_address=STRATEGY_ADDRESS
        )
        logger.info(f"Strategy deployed successfully. Tx hash: {receipt['transactionHash'].hex()}")
    except Exception as e:
        logger.error(f"Strategy deployment failed: {e}", exc_info=True)

async def schedule_strategy_deployment(strategy: dict):
    if not scheduler.running:
        scheduler.start()
    
    scheduler.add_job(
        strategy_deployment_job,
        args=[strategy],
        next_run_time=datetime.now()
    )

async def shutdown():
    if scheduler.running:
        scheduler.shutdown(wait=True)
