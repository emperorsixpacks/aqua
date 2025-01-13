import asyncio
from functools import wraps
from typing import Callable, Any


def retry(retries: int = 3, delay: float = 1.0):
    """
    Retry decorator for async functions.

    Args:
        retries (int): Number of retry attempts. Defaults to 3.
        delay (float): Delay between retries in seconds. Defaults to 1.0.

    Returns:
        Callable: Decorated function with retry logic.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt < retries - 1:
                        await asyncio.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator
