import asyncio
import uuid
import logging
from datetime import datetime

from fastapi import (
    HTTPException,
    status,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
)
from redis.exceptions import RedisError, ConnectionError, TimeoutError

from ..utils.rooms_utils import generate_room_key
from ..db.redis import redis_client

logger = logging.getLogger(__name__)


async def create_room_service(room_name: str, room_owner: str):
    """
    Creates a new room with the provided details and stores it in Redis.
    The room will have a unique access key and will expire after 2 hours.
    Args:
        room_details (createRoomsRequest): The details of the room to be created.
    Returns:
        createRoomsResponse: The response containing the room owner and access key.
    """
    try:
        access_key = await asyncio.to_thread(generate_room_key)
        room_id = str(uuid.uuid4())

        await redis_client.hset(
            name=f"room:{room_id}",
            mapping={
                "room_name": f"{room_name}",
                "room_owner": f"{room_owner}",
                "room_access_key": f"{access_key}",
                "created_at": f"{datetime.date(datetime.now())}",
            },
        )
        await redis_client.expire(name=f"room:{room_id}", time=7200)

        await redis_client.set(name=f"key:{access_key}", value=room_id, ex=7200)
        return {"room_owner": room_owner, "room_access_key": access_key}

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


async def join_room_service(websocket: WebSocket):

    username = websocket.query_params.get("username")
    access_key = websocket.query_params.get("room_access_key")

    if not username and not access_key:
        await websocket.close()
        raise WebSocketException(
            code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
            reason="please fill the required fields",
        )

    room_id = await redis_client.get(f"key:{access_key}")
    if not room_id:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="wrong creadentials try again.",
        )
        return
