"""room routers entry point"""

from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Request, status, Form
from fastapi.templating import Jinja2Templates


from backend.src.schemas.rooms import (
    CreateRoomsRequest,
    CreateRoomsResponse,
    JoinRoomRequest,
)
from backend.src.services.room_services import create_room_service, join_room_service
from backend.src.db.redis import redis_client

Router = APIRouter(tags=["chat-room"], prefix="/rooms")

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# <---------------------------------------------- GET --------------------------------------------->


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
    return templates.TemplateResponse(
        request=req,
        name="layouts/main_layout.jinja",
        context={
            "page_template": "pages/chat_window.jinja",
            "room_id": room_id,
            "user_id": user_id,
        },
    )


# <---------------------------------------------- POST -------------------------------------------->


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
