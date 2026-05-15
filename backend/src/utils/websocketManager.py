"""
WebSocket connection manager utilities for the cifrar-chat backend.

This module provides the WebsocketConnectionManager class, which handles the lifecycle
and management of WebSocket connections for chat rooms, including:
- Accepting and tracking new WebSocket connections per room.
- Broadcasting messages to clients in a room.
- Maintaining the mapping of active client connections in memory and in Redis.

Intended to be used as the backend WebSocket session handler for real-time chat features.
"""

import json
from datetime import datetime
from collections import defaultdict
from fastapi import WebSocket

from ..db.redis import redis_client


class WebsocketConnectionManager:
    """
    This class provides methods to handle WebSocket connection lifecycles, including connecting,
    disconnecting, and tracking clients in active chat rooms.
    """

    def __init__(self):
        self.active_rooms: dict[str, dict[str, WebSocket]] = defaultdict(list)

    async def accept_connection(
        self, websocket: WebSocket, room_id: str, connection_id: str
    ):
        """
        Accepts a new WebSocket connection for a given room and connection ID.
        """
        await websocket.accept()
        self.active_rooms[room_id][connection_id] = websocket
        # store room:connections
        await redis_client.sadd(f"room:{room_id}:connections", connection_id)
        await redis_client.expire(name=f"room:{room_id}:connections", time=7200)

    async def brodcast_message(
        self,
        connection_id: str,
        receive_msg: str,
        message_type: str = "chat-message",
    ):
        # get user:user_id who send the meessage
        username = await redis_client.hget(
            name=f"connection:{connection_id}", key="username"
        )
        # get room_id which user subscribe
        room_id = await redis_client.hget(
            name=f"connection:{connection_id}", key="room_id"
        )

        # strucure msg details
        message_details = {
            "type": message_type,
            "username": username,
            "message": receive_msg,
            "timestamp": datetime.now().strftime("%d-%b-%I:%M%p").lower(),
        }
        # convert into json string
        message_str = json.dumps(message_details)

        for conn in self.active_rooms[room_id].values():
            await conn.send_text(message_str)

    async def disconnect(self, room_id: str, connection_id: str):
        del self.active_rooms[room_id][connection_id]
        # delete


connection_manager = WebsocketConnectionManager()
