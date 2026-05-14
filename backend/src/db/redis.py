"""
Redis database client module for cifrar-chat application.

Handles asynchronous connection setup, health checking, and teardown for Redis,
using configuration from settings. Exposes a single redis_client instance for use
across the backend, plus utility functions to check and close the connection reliably.

Raises informative errors if Redis is unavailable on startup or shutdown.
"""

import logging
import redis.asyncio as redis_async
from redis.exceptions import (
    RedisError,
    TimeoutError as RedisTimeoutError,
    TryAgainError as RedisTryAgainError,
    ConnectionError as RedisConnectionError,
)

from ..core.settings import settings

logger = logging.getLogger(__name__)

redis_client = redis_async.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    username=settings.redis_username,
    decode_responses=True,
    retry_on_timeout=True,
    socket_timeout=5,
    socket_connect_timeout=5,
)


# function to check redis connection
async def check_redis_connection() -> None:
    """
    Check if the Redis connection is alive and raise an explicit error if not.

    Raises:
        RuntimeError: If Redis is unavailable or ping fails.
    """
    try:
        pong = await redis_client.ping()
        if pong is True:
            logger.info("Redis connection established successfully.")
        else:
            logger.warning("Received unexpected response from Redis ping: %s", pong)
            raise RuntimeError("Unexpected Redis ping response.")
    except (
        RedisError,
        RedisTimeoutError,
        RedisTryAgainError,
        RedisConnectionError,
    ) as error:
        logger.error("Redis connection failed: %s", error)
        raise RuntimeError("Redis is unavailable.") from error


# func to close redis connection
async def close_redis_connection():
    """
    Gracefully closes the Redis connection, logging the outcome.

    Raises:
        RuntimeError: If an error occurs when closing the Redis connection.
    """
    try:
        await redis_client.close()
        # Optionally, redis_client.close() may return None or awaitable. Log for debugging.
        logger.info("Redis connection closed successfully.")
    except (
        RedisError,
        RedisConnectionError,
        RedisTimeoutError,
        RedisTryAgainError,
    ) as error:
        logger.exception("Error closing Redis connection: %s", error)
        raise RuntimeError("Failed to close Redis connection.") from error
