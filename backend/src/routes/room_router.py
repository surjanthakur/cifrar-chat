"""room routers entry point"""

from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Request, status, Form, WebSocket
from fastapi.templating import Jinja2Templates


from ..schemas.rooms import (
    CreateRoomsRequest,
    CreateRoomsResponse,
    JoinRoomRequest,
)
from ..services.room_services import (
    create_room_service,
    join_room_service,
    realtime_chat_service,
)
from ..db.redis import redis_client

Router = APIRouter(tags=["chat-room"], prefix="/rooms")

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# <---------------------------------------------- GET ROUTES --------------------------------------------->


@Router.get("/create", summary="Render create room page")
async def render_create_room_form(request: Request):
    """Render the create room form page."""
    return templates.TemplateResponse(
        request=request,
        name="layouts/main_layout.jinja",
        context={"page_template": "pages/createRoomForm.jinja"},
    )


@Router.get("/join", summary="Render join room page")
async def render_join_room_form(req: Request, room_id: Optional[str] = None):
    """
    Render the join room form page.

    If a room_id is provided, gets room data from Redis and passes it to the template.
    """
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


@Router.get("/chats/on", summary="Render chat room page")
async def render_chat_window_page(
    req: Request,
    room_id: str,
    user_id: str,
):
    """Render the chat window page for a given room and user."""
    room_data = await redis_client.hgetall(f"room:{room_id}")
    username = await redis_client.hget(f"user:{user_id}", "username")
    online_count = await redis_client.scard(f"room:{room_id}:users")

    return templates.TemplateResponse(
        request=req,
        name="layouts/chat_layout.jinja",
        context={
            "room_id": room_id,
            "user_id": user_id,
            "username": username or "unknown",
            "room_name": (
                room_data.get("room_name", "Chat room") if room_data else "Chat room"
            ),
            "online_count": online_count or 0,
        },
    )


# <---------------------------------------------- POST ROUTES -------------------------------------------->


# create room
@Router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateRoomsResponse,
    summary="Create a new chat room",
)
async def create_room(
    room_name: str = Form(...),
    room_owner: str = Form(...),
):
    """Create a new chat room using room name and room owner."""
    room_details = CreateRoomsRequest(room_name=room_name, room_owner=room_owner)
    return await create_room_service(room_details)


# join room
@Router.post("/join", status_code=status.HTTP_201_CREATED)
async def join_room(
    username: str = Form(...),
    room_access_key: str = Form(...),
):
    """Join a chat room using room access key and username."""
    room_details = JoinRoomRequest(username=username, room_access_key=room_access_key)
    return await join_room_service(room_details)


# brodcasting chats
@Router.websocket("/ws/chat")
async def websockets_chats(websocket: WebSocket):
    return await realtime_chat_service(websocket)
