import logging
from app.services.market_service import MarketService

logger = logging.getLogger("market_job")
logging.basicConfig(level=logging.INFO)

class MarketDataJob:
    """
    A class to handle market data fetching and saving as a scheduled job.
    """

    @staticmethod
    async def fetch_and_save_market_data() -> None:
        """
        Fetches market data asynchronously and saves it to Pinecone via the MarketService.
        """
        try:
            logger.info("Starting market data fetch job...")

            market_data = await MarketService.fetch_market_data()
            
            if market_data:
                await MarketService.save_market_data(market_data)
                logger.info("Market data saved successfully!", market_data)
            else:
                logger.warning("No market data to save.")

        except Exception as e:
            logger.error(f"Error fetching and saving market data: {e}")
