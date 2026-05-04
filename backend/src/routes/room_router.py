from fastapi import APIRouter, status
from ..schemas.rooms import createRoomsRequest, createRoomsResponse
from ..services.room_services import create_rooms

Router = APIRouter(tags=["chat-rooms"], prefix="/rooms")


@Router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=createRoomsResponse,
    summary="Create a new chat room",
    description="Endpoint to create a new chat room. Requires a unique room name and room owner.",
)
def create_room(room_data: createRoomsRequest):
    """
    :param room_data: The data required to create a new chat room, including the room name and owner name.
    :type room_data: createRoomsRequest
    :return: A response containing the details of the created chat room.
    """
    return create_rooms(room_details=room_data)
