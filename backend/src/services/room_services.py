from fastapi import HTTPException, status
from redis.exceptions import RedisError, ConnectionError, TimeoutError
from datetime import datetime
from ..schemas.rooms import createRoomsRequest, createRoomsResponse
from ..utils.rooms_utils import generate_room_key
from ..db.redis import redis_client
import asyncio
import uuid
import logging

logger = logging.getLogger(__name__)


async def create_rooms(room_details: createRoomsRequest) -> createRoomsResponse:
    """
    Creates a new room with the provided details and stores it in Redis.
    The room will have a unique access key and will expire after 2 hours.
    Args:
        room_details (createRoomsRequest): The details of the room to be created.
    Returns:
        createRoomsResponse: The response containing the room owner and access key.
    """
    try:
        access_key = asyncio.to_thread(generate_room_key)
        room_id = str(uuid.uuid4())

        redis_client.hset(
            name=f"room:{room_id}",
            mapping={
                "room_name": f"{room_details.room_name}",
                "room_owner": f"{room_details.room_owner}",
                "room_access_key": f"{access_key}",
                "created_at": f"{datetime.date(datetime.now())}",
            },
        )
        redis_client.hexpire(name=f"room:{room_id}", seconds=7200)

        return createRoomsResponse(
            room_owner=room_details.room_owner, room_access_key=access_key
        )
    except (RedisError, ConnectionError, TimeoutError) as redis_err:
        logger.exception(msg=f"redis error while creating room: {redis_err}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="service is currently unavailable, try again later!",
        )
    except Exception as err:
        logger.exception(msg=f"error while creating room: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="something went wrong try again!",
        )
