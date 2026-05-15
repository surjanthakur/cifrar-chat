"""
Utilities for room management in the cifrar-chat backend.

This module provides helper functions and classes for handling room-related
operations, such as generating unique room keys and managing user storage in
Redis. These utilities are used by higher-level service layers to orchestrate
chat room creation, user joining, and membership persistence, ensuring secure
and efficient operation of the chat backend.

Functions/classes:
- generate_room_key: Generates secure unique access keys for chat rooms.
- ManageUserStore: Manages user-to-room mapping and user info lifecycle in Redis.

All Redis operations performed by these utilities are asynchronous.
"""

import secrets
import json
import asyncio
import logging
from datetime import datetime

from ..db.redis import redis_client
from ..utils.websocketManager import connection_manager

logger = logging.getLogger(__name__)


def generate_room_key():
    """
    Generates a unique room key using the secrets module for secure random generation.
    """
    return secrets.token_urlsafe(nbytes=10)


async def redis_room_listener():
    """
    Listens on Redis `room:*` channels and forwards chat payloads to every
    active WebSocket client in that room.
    """
    pubsub = redis_client.pubsub()
    await pubsub.psubscribe("room:*")

    while True:
        message = await pubsub.get_message(
            ignore_subscribe_messages=True,
            timeout=1.0,
        )
        if not message or message.get("type") != "pmessage":
            await asyncio.sleep(0.01)
            continue

        channel = message.get("channel", "")
        room_id = channel.removeprefix("room:") if channel.startswith("room:") else ""
        raw = message.get("data")
        if not room_id or not raw:
            await asyncio.sleep(0.01)
            continue

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {
                "type": "chat_message",
                "username": "unknown",
                "message": raw,
                "timestamp": datetime.now().strftime("%d-%b-%I:%M%p").lower(),
            }

        if "timestamp" not in payload:
            payload["timestamp"] = datetime.now().strftime("%d-%b-%I:%M%p").lower()

        await connection_manager.broadcast_to_room(room_id, payload)
        await asyncio.sleep(0.01)


class ManageUserStore:
    """
    ManageUserStore handles storage and management of user-related data in Redis.
    """

    def __init__(self):
        """
        Initializes the ManageUserStore class.
        """

    async def add_user(
        self,
        username: str,
        room_id: str,
        user_id: str,
        access_key: str,
        connection_id: str,
    ):
        """
        Store the user's info in Redis under 'user:{user_id}' hash.
        """
        await redis_client.hset(
            name=f"user:{user_id}",
            mapping={
                "username": f"{username}",
                "connection_id": f"{connection_id}",
                "room_access_key": f"{access_key}",
                "room_id": f"{room_id}",
            },
        )
        await redis_client.expire(name=f"user:{user_id}", time=7200)

    async def add_user_in_room(self, room_id: str, user_id: str):
        """
        Add a user to the set of users in a specified room in Redis.
        """
        await redis_client.sadd(f"room:{room_id}:users", user_id)
        await redis_client.expire(f"room:{room_id}:users", 7200)

    async def add_users_connections(self, user_id: str, connection_id: str):
        """
        Add a connection ID to a user's connections set in Redis.
        """
        await redis_client.sadd(f"users:{user_id}:connections", connection_id)
        await redis_client.expire(f"users:{user_id}:connections", 7200)

    async def add_connection(
        self,
        username: str,
        connection_id: str,
        user_id: str,
        room_id: str,
    ):
        """
        Store connection information, mapping a connection ID to a user and room.
        """
        await redis_client.hset(
            name=f"connection:{connection_id}",
            mapping={
                "username": f"{username}",
                "user_id": f"{user_id}",
                "room_id": f"{room_id}",
            },
        )
        await redis_client.expire(name=f"connection:{connection_id}", time=7200)


redisUserManager = ManageUserStore()
