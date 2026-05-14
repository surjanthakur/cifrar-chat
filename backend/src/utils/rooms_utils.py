import secrets
import json
from datetime import datetime
from fastapi import WebSocket
from collections import defaultdict
from ..db.redis import redis_client


def generate_room_key():
    """
    Generates a unique room key using the secrets module for secure random generation.
    """
    return secrets.token_urlsafe(nbytes=10)


class WebsocketConnectionManager:
    """
    This class provides methods to handle WebSocket connection lifecycles, including connecting,
    disconnecting, and tracking clients in active chat rooms.
    """

    def __init__(self):
        self.active_rooms: dict[str, list[WebSocket]] = defaultdict(list)

    async def accept_connection(
        self, websocket: WebSocket, room_id: str, connection_id: str
    ):
        """
        Accepts a new WebSocket connection for a given room and connection ID.
        """
        await websocket.accept()
        self.active_rooms[room_id].append(websocket)
        # store room:connections
        await redis_client.sadd(f"room:{room_id}:connections", connection_id)
        await websocket.send_text(json.dumps({"status": "success", "room_id": room_id}))

    async def brodcast_message(self, connection_id: str, receive_msg: str):
        # get user:user_id who send the meessage
        user_id = await redis_client.hget(
            name=f"connection:{connection_id}", key="user_id"
        )
        # get the user:username
        username = await redis_client.hget(name=f"user:{user_id}", key="username")
        # get room_id which user subscribe
        room_id = await redis_client.hget(
            name=f"connection:{connection_id}", key="room_id"
        )

        # strucure msg details
        message_details = {
            "username": username,
            "message": receive_msg,
            "timestamp": datetime.now().strftime("%d-%b-%I:%M%p").lower(),
        }

        # convert into json string
        message_str = json.dumps(message_details)

        for connection in self.active_rooms[room_id]:
            # send in each WS connections
            await connection.send_text(message_str)


connection_manager = WebsocketConnectionManager()
