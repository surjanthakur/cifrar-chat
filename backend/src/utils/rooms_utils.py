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
from backend.src.db.redis import redis_client


def generate_room_key():
    """
    Generates a unique room key using the secrets module for secure random generation.
    """
    return secrets.token_urlsafe(nbytes=10)


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

    async def add_connection(self, connection_id: str, user_id: str, room_id: str):
        """
        Store connection information, mapping a connection ID to a user and room.
        """
        await redis_client.hset(
            name=f"connection:{connection_id}",
            mapping={
                "user_id": f"{user_id}",
                "room_id": f"{room_id}",
            },
        )
        await redis_client.expire(name=f"connection:{connection_id}", time=7200)


redisUserManager = ManageUserStore()
