"""
Room services module for cifrar-chat backend.

This module provides async service functions for handling room creation,
joining, and management, leveraging Redis as the main storage backend.

Functions here are intended to orchestrate business logic for room lifecycles,
including creation with unique access keys, expiring room state, and integrating
with user and websocket management utilities.

All Redis operations are asynchronous and resilient to transient database
errors.
"""

import asyncio
import uuid
import json
import logging
from datetime import datetime

from fastapi import (
    HTTPException,
    WebSocket,
    status,
    WebSocketException,
    WebSocketDisconnect,
)
from fastapi.responses import RedirectResponse
from redis.exceptions import (
    RedisError,
    ConnectionError as RedisConnectionError,
    TimeoutError as RedisTimeoutError,
)


from ..utils.rooms_utils import generate_room_key, redisUserManager
from ..db.redis import redis_client
from ..schemas.rooms import CreateRoomsRequest, JoinRoomRequest
from ..utils.websocketManager import connection_manager

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
        await redisUserManager.add_connection(
            form_data.username,
            user_connection_id,
            user_id,
            room_id,
        )

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


# websocket endpoint
async def realtime_chat_service(websocket: WebSocket):
    room_id = websocket.query_params.get("room_id")
    user_id = websocket.query_params.get("user_id")

    if not room_id or not user_id:
        await websocket.close()
        raise WebSocketException(
            code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
            reason="invalid data try again!",
        )
    user_connection_id = await redis_client.hget(
        name=f"user:{user_id}", key="connection_id"
    )
    if not user_connection_id:
        await websocket.close()
        raise WebSocketException(
            code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
            reason="invalid data try again!",
        )

    username = await redis_client.hget(name=f"user:{user_id}", key="username")

    await connection_manager.accept_connection(
        websocket=websocket,
        room_id=room_id,
        connection_id=user_connection_id,
    )
    await connection_manager.brodcast_message(
        connection_id=user_connection_id,
        receive_msg=f"{username or 'Someone'} joined the room",
        message_type="user_joined",
    )

    try:
        while True:
            message = await websocket.receive_text()
            payload = json.dumps(
                {
                    "type": "chat_message",
                    "username": username or "unknown",
                    "message": message,
                    "timestamp": datetime.now().strftime("%d-%b-%I:%M%p").lower(),
                }
            )
            await redis_client.publish(channel=f"room:{room_id}", message=payload)

    except WebSocketDisconnect:
        await connection_manager.brodcast_message(
            connection_id=user_connection_id,
            receive_msg=f"{username or 'Someone'} left the room",
            message_type="user_left",
        )
        await connection_manager.disconnect(room_id, user_connection_id, user_id)
