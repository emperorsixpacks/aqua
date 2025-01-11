from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

from jobs.market_job import MarketDataJob



def schduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=lambda: asyncio.run(MarketDataJob.fetch_and_save_market_data()),
        trigger="interval",
        hours=24 
    )
    scheduler.start()
    print("Market job scheduled to run every 24 hours.")