from fastapi import (
    APIRouter,
    Request,
    status,
    WebSocket,
)
from fastapi.templating import Jinja2Templates
from pathlib import Path

from ..schemas.rooms import createRoomsRequest, createRoomsResponse
from ..services.room_services import create_room_service, join_room_service

Router = APIRouter(tags=["chat-room"], prefix="/rooms")

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=TEMPLATE_DIR)


@Router.get(
    "/create-rooms",
    summary="Render create room page",
    status_code=status.HTTP_200_OK,
)
async def create_room_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="layouts/main_layout.jinja",
        context={"page_template": "pages/createRoomForm.jinja"},
    )


@Router.get(
    "/join-rooms",
    summary="Render join room page",
    status_code=status.HTTP_200_OK,
)
async def join_room_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="layouts/main_layout.jinja",
        context={"page_template": "pages/joinRoomForm.jinja"},
    )


# create room
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


# join room
@Router.websocket("/join")
async def join_room_websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for joining a chat room.

    This endpoint allows clients to join a chat room via a WebSocket connection.
    The client must provide their username and the room's access key as query parameters.
    Upon successful connection, the user is added to the room and their connection details are tracked.
    """
    return await join_room_service(websocket)
