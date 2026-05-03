from pydantic import BaseModel, Field


class createRoomsRequest(BaseModel):
    room_owner: str = Field(
        ...,
        min_length=2,
        max_length=15,
        regex=r"^[a-zA-Z0-9_]+$",
        title="Room Owner",
        description="The username of the room owner. It should be between 2 and 15 characters long and can only contain letters, numbers, and underscores.",
    )
    room_name: str = Field(
        ...,
        min_length=3,
        max_length=20,
        regex=r"^[a-zA-Z0-9_ ]+$",
        title="Room Name",
        description="The name of the room. It should be between 3 and 20 characters long and can only contain letters, numbers, spaces, and underscores.",
    )


class createRoomsResponse(BaseModel):
    room_owner: str
    room_access_key: str
