import secrets
from fastapi import WebSocket, WebSocketDisconnect
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
        self.active_connections = {}

    async def accept_connection(
        self, websocket: WebSocket, room_id: str, connection_id: str
    ):
        """
        Accepts a new WebSocket connection for a given room and connection ID.

        Args: websocket (WebSocket): The WebSocket connection to accept.
        room_id (str): The unique identifier of the room the user is joining.
        connection_id (str): The unique identifier for this WebSocket connection.

        This method accepts the WebSocket connection and registers it in the
        active connections dictionary as well as adds the connection ID to
        the Redis set of active connections for the specified room.
        """
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
        """
        Adds user and connection details to Redis for tracking room membership and connections.

        Args:
            username (str): The username of the client joining the room.
            access_key (str): The access key associated with the room.
            user_id (str): The unique identifier of the user.
            room_id (str): The unique identifier of the room.
            connection_id (str): The unique identifier for the client's WebSocket connection.

        This method stores the user information, associates the user with the room,
        tracks the connection, and ensures the connection details are available in Redis.
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
        await redis_client.sadd(f"room:{room_id}:users", user_id)
        await redis_client.sadd(f"users:{user_id}:connections", connection_id)
        await redis_client.hset(
            name=f"connection:{connection_id}",
            mapping={
                "user_id": f"{user_id}",
                "room_id": f"{room_id}",
            },
        )

    async def brodcast_messages():
        """function to brodcast messages in websocket connections"""
        pass


socketManager = WebsocketConnectionManager()
