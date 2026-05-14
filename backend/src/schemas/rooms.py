"""
Schemas for chat room creation and joining within the cifrar-chat application.

Defines request and response models for room-related endpoints using Pydantic BaseModel.
"""

from pydantic import BaseModel, Field


class CreateRoomsRequest(BaseModel):
    """Request schema for creating a chat room."""

    room_owner: str = Field(
        ...,
        min_length=2,
        max_length=15,
        title="Room Owner",
    )
    room_name: str = Field(
        ...,
        min_length=3,
        max_length=20,
        title="Room Name",
    )


class CreateRoomsResponse(BaseModel):
    """Response schema for room creation."""

    room_owner: str
    room_access_key: str


class JoinRoomRequest(BaseModel):
    """Request schema for joining a chat room."""

    username: str = Field(
        ...,
        min_length=2,
        max_length=15,
        title="username",
    )
    room_access_key: str = Field(
        ...,
        min_length=10,
        title="room_access_key",
    )
