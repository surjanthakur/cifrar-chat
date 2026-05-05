import secrets
from fastapi import WebSocket
from ..db.redis import redis_client


def generate_room_key():
    """
    Generates a unique room key using the secrets module for secure random generation.
    """
    return secrets.token_urlsafe(nbytes=10)


class WebsocketConnectionManager:
    """
    Manages active WebSocket connections for chat rooms.

    This class provides methods to handle WebSocket connection lifecycles, including connecting,
    disconnecting, and tracking clients in active chat rooms.
    """

    def __init__(self):
        self.active_connections = dict[str, WebSocket] = {}

    async def accept_connection(
        self, websocket: WebSocket, room_id: str, connection_id: str
    ):
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        await redis_client.sadd(f"room:{room_id}:connections", connection_id)

    async def add_to_redis(
        self,
        username: str,
        access_key: str,
        user_id: str,
        room_id: str,
        connection_id: str,
    ):
        await redis_client.hset(
            name=f"user:{user_id}",
            mapping={
                "username": f"{username}",
                "connection_id": f"{connection_id}",
                "room_access_key": f"{access_key}",
                "room_id": f"{room_id}",
            },
        )
        await redis_client.sadd(f"room:{room_id}:users", user_id)
        await redis_client.sadd(f"users:{user_id}:connections", connection_id)
        await redis_client.hset(
            name=f"connection:{connection_id}",
            mapping={
                "user_id": f"{user_id}",
                "room_id": f"{room_id}",
            },
        )


socketManager = WebsocketConnectionManager()
