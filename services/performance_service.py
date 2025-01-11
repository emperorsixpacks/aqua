import logging
from datetime import datetime
from typing import Dict, List, Optional

from utils.pinecone_client import fetch, natural_query, save

logger = logging.getLogger("PERFORMANCE_SERVICE")
logging.basicConfig(level=logging.INFO)

class PerformanceService:
    """
    Service to manage strategies: saving, updating performance, fetching, and querying.
    """
    @staticmethod
    def get_latest_performance_data() -> Dict:
        """
        Fetch latest performance data.

        Returns:
            Dict: The most recent performance data.
        """
        try:
            results = natural_query("Latest performance data", limit=1)
            logger.info(f"Natural query results: {results}")

            if results:
                return results[0]["metadata"]["data"]
            return {}
        except Exception as e:
            logger.error(f"Error fetching performance data: {e}")
            return {}
    
    @staticmethod
    def save_strategy(strategy: Dict) -> None:
        """
        Save a generated strategy into Pinecone.

        Args:
            strategy (Dict): The strategy object to save. Must contain 'name', 'description', and other metadata.
        """
        try:
            logger.info("Saving a new strategy...")

            strategy_id = f"strategy_{int(datetime.utcnow().timestamp())}"

            performance_metrics = {
                "success_rate": 0,  
                "profit": 0, 
                "loss": 0,  
                "status": "active", 
                "history": []
            }

            metadata = {
                "name": strategy["name"],
                "description": strategy["description"],
                "minDeposit": strategy.get("minDeposit", "0"),
                "created_at": datetime.utcnow().isoformat(),
                **performance_metrics
            }

            save(
                key=strategy_id,
                metadata=metadata,
                text=strategy["description"] 
            )
            logger.info(f"Strategy saved successfully with ID: {strategy_id}")

        except Exception as e:
            logger.error(f"Error saving strategy: {e}")

    @staticmethod
    def update_strategy(strategy_id: str, update_data: Dict) -> None:
        """
        Update the performance metrics of a saved strategy.

        Args:
            strategy_id (str): The unique ID of the strategy to update.
            update_data (Dict): The updated performance metrics (e.g., profit, success_rate).
        """
        try:
            logger.info(f"Updating strategy performance for ID: {strategy_id}")

            strategy = fetch(strategy_id)
            if not strategy:
                logger.warning(f"No strategy found with ID: {strategy_id}")
                return

            metadata = strategy["metadata"]
            metadata.update(update_data)

            metadata.setdefault("history", []).append({
                "timestamp": datetime.utcnow().isoformat(),
                **update_data
            })

            save(key=strategy_id, metadata=metadata, text=metadata["description"])
            logger.info(f"Strategy performance updated successfully for ID: {strategy_id}")

        except Exception as e:
            logger.error(f"Error updating strategy performance: {e}")

    @staticmethod
    def fetch_strategy(strategy_id: str) -> Optional[Dict]:
        """
        Fetch a strategy along with its performance data.

        Args:
            strategy_id (str): The unique ID of the strategy to fetch.

        Returns:
            Optional[Dict]: The strategy with its metadata and performance data.
        """
        try:
            logger.info(f"Fetching strategy with ID: {strategy_id}")

            strategy = fetch(strategy_id)
            if strategy:
                logger.info(f"Fetched strategy: {strategy_id}")
                return strategy
            else:
                logger.warning(f"No strategy found with ID: {strategy_id}")
                return None

        except Exception as e:
            logger.error(f"Error fetching strategy: {e}")
            return None

    @staticmethod
    def fetch_strategies(filter_criteria: Optional[Dict] = None, limit: int = 10) -> List[Dict]:
        """
        Fetch saved strategies from Pinecone using metadata filtering.

        Args:
            filter_criteria (Optional[Dict]): Metadata filters for strategies.
            limit (int): Maximum number of strategies to fetch.

        Returns:
            List[Dict]: A list of strategies, including their IDs and metadata.
        """
        try:
            logger.info("Fetching saved strategies from Pinecone...")
            strategies = fetch(key="all")  
            logger.info(f"Fetched {len(strategies)} strategies.")
            return strategies[:limit]

        except Exception as e:
            logger.error(f"Error fetching strategies: {e}")
            return []

    @staticmethod
    def query_strategies(query: str, limit: int = 5) -> List[Dict]:
        """
        Query Pinecone for strategies using a plain English query.

        Args:
            query (str): The natural language query to search strategies.
            limit (int): The maximum number of results to return.

        Returns:
            List[Dict]: A list of matching strategies with metadata.
        """
        try:
            logger.info(f"Querying strategies with plain English: '{query}'")
            strategies = natural_query(query=query, limit=limit)
            logger.info(f"Found {len(strategies)} strategies matching the query: '{query}'")
            return strategies

        except Exception as e:
            logger.error(f"Error querying strategies: {e}")
            return []

    
