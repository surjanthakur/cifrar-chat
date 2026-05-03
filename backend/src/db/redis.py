import logging
import redis.asyncio as redis
from redis.exceptions import RedisError, TimeoutError, TryAgainError, ConnectionError
from ..core.settings import settings

logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    username=settings.redis_username,
    decode_responses=True,
    retry_on_timeout=True,
)


# function to check redis connection
async def check_redis_connection() -> None:
    try:
        await redis_client.ping()
        logger.info(msg="redis connection established successfully.")
    except (RedisError, TimeoutError, TryAgainError, ConnectionError) as error:
        logger.warning(msg=f"Redis connection failed: {error}")
        raise RuntimeError("redis is unavailable.") from error


# func to close redis connection
async def close_redis_connection():
    try:
        await redis_client.close()
        logger.info(msg="redis connection closed")
    except (RedisError, ConnectionError) as error:
        logger.warning(msg=f"redis connection error while closing connection:: {error}")
        raise RuntimeError(
            "redis connection error while closing connection."
        ) from error
