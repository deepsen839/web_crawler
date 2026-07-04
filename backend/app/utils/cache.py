from cachetools import TTLCache
from functools import wraps
from typing import Any, Callable
import asyncio


# Cache stores up to 100 items for 1 hour
cache = TTLCache(maxsize=100, ttl=3600)


def cached(func: Callable):
    """
    Simple async cache decorator.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):

        key = (
            func.__name__,
            str(args),
            str(sorted(kwargs.items())),
        )

        if key in cache:
            return cache[key]

        result = await func(*args, **kwargs)

        cache[key] = result

        return result

    return wrapper


def clear_cache():
    """
    Clear all cached items.
    """
    cache.clear()