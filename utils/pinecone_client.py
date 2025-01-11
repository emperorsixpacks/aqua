import os
import logging
from typing import Dict, List, Optional
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

pinecone_api_key = os.getenv("PINECONE_API_KEY", "")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT", "")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "")

if not pinecone_api_key or not pinecone_environment or not pinecone_index_name:
    logger.error("Missing required Pinecone environment variables.")
    raise EnvironmentError("Ensure PINECONE_API_KEY, PINECONE_ENVIRONMENT, and PINECONE_INDEX_NAME are set.")

pinecone_client = Pinecone(api_key=pinecone_api_key)

try:
    existing_indexes = [index.name for index in pinecone_client.list_indexes()]
    if pinecone_index_name not in existing_indexes:
        logger.info("Creating Pinecone index: %s", pinecone_index_name)
        pinecone_client.create_index(
            name=pinecone_index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=pinecone_environment
            )
        )
    index = pinecone_client.Index(pinecone_index_name)
    logger.info("Pinecone index initialized: %s", pinecone_index_name)
except Exception as e:
    logger.error("Error initializing Pinecone index: %s", str(e))
    raise

try:
    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")
    logger.info("OpenAI Embedding model initialized.")
except Exception as e:
    logger.error("Error initializing embedding model: %s", str(e))
    raise


def generate_embedding(text: str) -> List[float]:
    """
    Generates an embedding for the given text.

    Args:
        text (str): Text to generate embedding for.

    Returns:
        List[float]: Generated embedding vector.
    """
    try:
        logger.info("Generating embedding for text: %s", text)
        return embedding_model.embed_query(text)
    except Exception as e:
        logger.error("Error generating embedding for text '%s': %s", text, str(e))
        raise


def save(key: str, metadata: Dict, text: str) -> None:
    """
    Saves data to the Pinecone index.

    Args:
        key (str): Unique identifier for the data.
        metadata (Dict): Metadata to store.
        text (str): Text to generate embedding and store.
    """
    try:
        logger.info("Saving data to Pinecone for key: %s", key)
        vector = generate_embedding(text)
        index.upsert([{"id": key, "values": vector, "metadata": metadata}])
        logger.info("Data saved successfully for key: %s", key)
    except Exception as e:
        logger.error("Error saving data for key '%s': %s", key, str(e))
        raise


def fetch(key: str) -> Optional[Dict]:
    """
    Fetches metadata from the Pinecone index for a given key.

    Args:
        key (str): Unique identifier for the data.

    Returns:
        Optional[Dict]: Metadata associated with the key, or None if not found.
    """
    try:
        logger.info("Fetching data from Pinecone for key: %s", key)
        response = index.fetch(ids=[key])
        if key in response.get("vectors", {}):
            return response["vectors"][key].get("metadata", {})
        logger.warning("No data found in Pinecone for key: %s", key)
        return None
    except Exception as e:
        logger.error("Error fetching data for key '%s': %s", key, str(e))
        raise


def update(key: str, metadata: Dict, text: str) -> None:
    """
    Updates data in the Pinecone index.

    Args:
        key (str): Unique identifier for the data.
        metadata (Dict): Metadata to update.
        text (str): Text to generate embedding and update.
    """
    try:
        logger.info("Updating data in Pinecone for key: %s", key)
        vector = generate_embedding(text)
        index.upsert([{"id": key, "values": vector, "metadata": metadata}])
        logger.info("Data updated successfully for key: %s", key)
    except Exception as e:
        logger.error("Error updating data for key '%s': %s", key, str(e))
        raise


def delete(key: str) -> None:
    """
    Deletes data from the Pinecone index.

    Args:
        key (str): Unique identifier for the data.
    """
    try:
        logger.info("Deleting data from Pinecone for key: %s", key)
        index.delete(ids=[key])
        logger.info("Data deleted successfully for key: %s", key)
    except Exception as e:
        logger.error("Error deleting data for key '%s': %s", key, str(e))
        raise


def natural_query(query: str, limit: int = 5) -> List[Dict]:
    """
    Query Pinecone using a natural language query.

    Args:
        query (str): The natural language query to search for data.
        limit (int): The maximum number of results to return.

    Returns:
        List[Dict]: A list of matching items, including their metadata and similarity scores.
    """
    try:
        logger.info(f"Performing natural query on Pinecone: '{query}'")

        query_vector = generate_embedding(query)  

        response = index.query(
            vector=query_vector, 
            top_k=limit,  
            include_metadata=True 
        )

        results = [
            {
                "id": match["id"], 
                "score": match["score"],  
                "metadata": match["metadata"] 
            }
            for match in response.get("matches", [])
        ]

        logger.info(f"Natural query found {len(results)} matching items.")
        return results

    except Exception as e:
        logger.error(f"Error performing natural query: {e}")
        return []
