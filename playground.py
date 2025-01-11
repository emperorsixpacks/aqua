import asyncio
from jobs.market_job import MarketDataJob

async def run_job():
    await MarketDataJob.fetch_and_save_market_data()

asyncio.run(run_job())
