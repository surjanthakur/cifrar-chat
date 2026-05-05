from fastapi import (
    APIRouter,
    status,
    WebSocket,
)
from ..schemas.rooms import createRoomsRequest, createRoomsResponse
from ..services.room_services import create_room_service

Router = APIRouter(tags=["chat-rooms"], prefix="/rooms")


@Router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=createRoomsResponse,
    summary="Create a new chat room",
    description="Endpoint to create a new chat room. Requires a unique room name and room owner.",
)
async def create_room(room_data: createRoomsRequest):
    """
    :param room_data: The data required to create a new chat room, including the room name and owner name.
    :type room_data: createRoomsRequest
    :return: A response containing the details of the created chat room.
    """
    return await create_room_service(
        room_name=room_data.room_name,
        room_owner=room_data.room_owner,
    )


@Router.websocket("/join")
async def join_room_websocket_endpoint(websocket: WebSocket):
    pass
