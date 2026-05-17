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
        self.active_rooms: dict[str, dict[str, WebSocket]] = defaultdict(dict)

    # accept the ws connection.
    async def accept_connection(
        self, websocket: WebSocket, room_id: str, connection_id: str
    ):
        """
        Accepts and registers a new WebSocket connection for a specified chat room.
        """

        await websocket.accept()
        self.active_rooms[room_id][connection_id] = websocket
        # store room:connections
        await redis_client.sadd(f"room:{room_id}:connections", connection_id)
        await redis_client.expire(name=f"room:{room_id}:connections", time=7200)

    # brodcast messages when user joined ,disconnect ,other reasons.
    async def brodcast_message(
        self,
        connection_id: str,
        receive_msg: str,
        message_type: str = "chat-message",
    ):
        """
        Broadcasts a message to all WebSocket connections in the sender's room.

        Args:
            connection_id (str): The connection ID of the sender.
            receive_msg (str): The message to broadcast.
            message_type (str, optional): The type of message. Defaults to "chat-message".

        This method:
            - Retrieves the sender's username and room ID from Redis using the connection ID.
            - Constructs a message payload including type, username, message, and timestamp.
            - Broadcasts the message to all activ  \e WebSocket connections in the room.
        """

        username = await redis_client.hget(
            name=f"connection:{connection_id}", key="username"
        )
        # get room_id which user is subscribed to
        room_id = await redis_client.hget(
            name=f"connection:{connection_id}", key="room_id"
        )

        # structure msg details
        message_details = {
            "type": message_type,
            "username": username,
            "message": receive_msg,
            "timestamp": datetime.now().strftime("%d-%b-%I:%M%p").lower(),
        }
        # convert into json string
        message_str = json.dumps(message_details)

        room_connections = self.active_rooms.get(room_id)
        if not room_connections:
            return

        for conn in room_connections.values():
            await conn.send_text(message_str)

    # brodcast user message to all ws connnection.
    async def broadcast_to_room(self, room_id: str, message_details: dict):
        """Send a JSON payload to every WebSocket client in a room."""
        room_connections = self.active_rooms.get(room_id)
        if not room_connections:
            return

        message_str = json.dumps(message_details)

        # storing dead [closed] connection id
        dead_connections = []

        for connection_id, conn in room_connections.items():

            try:
                await conn.send_text(message_str)
            except Exception:
                # append dead connection on [dead_connections list]
                dead_connections.append(connection_id)

        for conn_id in dead_connections:
            # remove dead connection [websocket obj]
            room_connections.pop(conn_id, None)

    # disconnect the ws connection after connection lost or error.
    async def disconnect(self, room_id: str, connection_id: str, user_id: str):
        """
        Disconnects a user's WebSocket session in a room, removes connection and user info from local memory
        and cleans up associated keys from Redis.

        Args:
            room_id (str): The ID of the room the user is leaving.
            connection_id (str): The unique connection identifier for the user.
            user_id (str): The unique user identifier.

        Performs the following cleanup:
            - Removes the WebSocket connection from in-memory active_rooms tracking.
            - Deletes the user's hash, connections set, and connection info from Redis.
            - Removes the user's connection and membership from the room in Redis.
        """
        room_connections = self.active_rooms.get(room_id)
        if room_connections and connection_id in room_connections:
            del room_connections[connection_id]
        if room_connections is not None and not room_connections:
            del self.active_rooms[room_id]

        await redis_client.delete(f"user:{user_id}")
        await redis_client.delete(f"users:{user_id}:connections")
        await redis_client.delete(f"connection:{connection_id}")
        await redis_client.srem(f"room:{room_id}:connections", connection_id)
        await redis_client.srem(f"room:{room_id}:users", user_id)


connection_manager = WebsocketConnectionManager()
