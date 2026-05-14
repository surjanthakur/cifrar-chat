"""
Room services module for cifrar-chat backend.

This module provides async service functions for handling room creation,
joining, and management, leveraging Redis as the main storage backend.

Functions here are intended to orchestrate business logic for room lifecycles,
including creation with unique access keys, expiring room state, and integrating
with user and websocket management utilities.

All Redis operations are asynchronous and resilient to transient database
errors.

Typical usage:
    from backend.src.services import room_services

    await room_services.create_room_service(your_createRoomsRequest_instance)
    # etc.
"""

import asyncio
import uuid
import logging
from datetime import datetime

from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from redis.exceptions import (
    RedisError,
    ConnectionError as RedisConnectionError,
    TimeoutError as RedisTimeoutError,
)


from backend.src.utils.rooms_utils import generate_room_key, redisUserManager
from backend.src.db.redis import redis_client
from backend.src.schemas.rooms import CreateRoomsRequest, JoinRoomRequest

logger = logging.getLogger(__name__)


# create room
async def create_room_service(room_data: CreateRoomsRequest):
    """
    Creates a new room with the provided details and stores it in Redis.
    The room will have a unique access key and will expire after 2 hours.
    """
    try:
        access_key = await asyncio.to_thread(generate_room_key)
        room_id = str(uuid.uuid4())
        time_to_live = 7200

        await redis_client.hset(
            name=f"room:{room_id}",
            mapping={
                "room_name": f"{room_data.room_name}",
                "room_owner": f"{room_data.room_owner}",
                "room_access_key": f"{access_key}",
                "created_at": f"{datetime.date(datetime.now())}",
            },
        )
        await redis_client.expire(name=f"room:{room_id}", time=time_to_live)
        await redis_client.set(name=f"key:{access_key}", value=room_id, ex=time_to_live)

        return RedirectResponse(
            url=f"/api/rooms/join?room_id={room_id}",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    except (RedisError, RedisConnectionError, RedisTimeoutError) as redis_err:
        logger.exception(msg=f"redis error while creating room: {redis_err}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="service is currently unavailable, try again later!",
        ) from redis_err
    except Exception as err:
        logger.exception(msg=f"error while creating room: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="something went wrong try again!",
        ) from err


# join room
async def join_room_service(form_data: JoinRoomRequest):
    """
    Join an existing room using the provided access key and username.

    Looks up the room by access key in Redis, creates a new user, and registers user-related
    info in Redis. Redirects to the chat window if successful. Raises HTTPException if the
    access key does not exist or in case of redis error or other failure.

    Args:
        form_data (JoinRoomRequest): Data containing username and room access key.

    Returns:
        RedirectResponse: Redirects to the chat window page with room and user info.
    """
    try:
        room_id = await redis_client.get(f"key:{form_data.room_access_key}")
        if not room_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wrong credential, try again.",
            )
        user_id = str(uuid.uuid4())
        user_connection_id = str(uuid.uuid4())

        # store users info
        await redisUserManager.add_user(
            username=form_data.username,
            room_id=room_id,
            user_id=user_id,
            access_key=form_data.room_access_key,
            connection_id=user_connection_id,
        )
        # store room:users
        await redisUserManager.add_user_in_room(room_id, user_id)
        # store users:connections
        await redisUserManager.add_users_connections(user_id, user_connection_id)
        # store connections_info
        await redisUserManager.add_connection(user_connection_id, user_id, room_id)

        # redirecting to chat
        return RedirectResponse(
            url=f"/api/rooms/chats/on?room_id={room_id}&user_id={user_id}",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    except HTTPException:
        raise

    except (RedisError, RedisConnectionError, RedisTimeoutError) as redis_err:
        logger.exception(msg=f"redis error while creating room: {redis_err}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="service is currently unavailable, try again later!",
        ) from redis_err

    except Exception as err:
        logger.exception(msg=f"error while joining room: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="something went wrong try again!",
        ) from err
