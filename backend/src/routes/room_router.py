from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Request, status, WebSocket, Form
from fastapi.templating import Jinja2Templates


from ..schemas.rooms import createRoomsResponse, createRoomsRequest
from ..services.room_services import create_room_service, join_room_service
from ..db.redis import redis_client

Router = APIRouter(tags=["chat-room"], prefix="/rooms")

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# render create room form
@Router.get("/create", summary="Render create room page")
async def render_create_room_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="layouts/main_layout.jinja",
        context={"page_template": "pages/createRoomForm.jinja"},
    )


# render join room form
@Router.get("/join", summary="Render join room page")
async def render_join_room_form(req: Request, room_id: Optional[str] = None):
    room_data = None

    if room_id:
        room_data = await redis_client.hgetall(f"room:{room_id}")

    return templates.TemplateResponse(
        request=req,
        name="layouts/main_layout.jinja",
        context={
            "page_template": "pages/joinRoomForm.jinja",
            "room": room_data,
        },
    )


# render chat room page
@Router.get("/chat/on", summary="Render chat room page")
async def render_chat_window_page(req: Request, room_name: str):
    return templates.TemplateResponse(
        request=req,
        name="/pages/chat_window.jinja",
        context={"room_name": room_name},
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
