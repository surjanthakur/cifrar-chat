from fastapi import APIRouter, Request, status, WebSocket, Form
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional

from ..schemas.rooms import createRoomsResponse, createRoomsRequest
from ..services.room_services import create_room_service, join_room_service
from ..db.redis import redis_client

Router = APIRouter(tags=["chat-room"], prefix="/rooms")

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=TEMPLATE_DIR)


@Router.get("/create", summary="Render create room page")
async def create_room_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="layouts/main_layout.jinja",
        context={"page_template": "pages/createRoomForm.jinja"},
    )


@Router.get("/join", summary="Render join room page")
async def join_room_page(request: Request, room_id: Optional[str] = None):
    room_data = None
    if room_id:
        room_data = redis_client.hget(f"room:{room_id}")
    return templates.TemplateResponse(
        request=request,
        name="layouts/main_layout.jinja",
        context={
            "page_template": "pages/joinRoomForm.jinja",
            "room": room_data,
        },
    )


# create room
@Router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=createRoomsResponse,
    summary="Create a new chat room",
    description="Endpoint to create a new chat room. Requires a unique room name and room owner.",
)
async def create_room(
    room_name: str = Form(...),
    room_owner: str = Form(...),
):
    """
    :param room_data: The data required to create a new chat room, including the room name and owner name.
    :type room_data: createRoomsRequest
    :return: A response containing the details of the created chat room.
    """
    room_details = createRoomsRequest(room_name=room_name, room_owner=room_owner)
    return await create_room_service(room_details)


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
