import secrets
from fastapi import WebSocket


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
        self.active_connections = list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
