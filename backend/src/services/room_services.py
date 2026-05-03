from fastapi import HTTPException, status
from ..schemas.rooms import createRoomsRequest, createRoomsResponse


async def create_rooms(room_details: createRoomsRequest) -> createRoomsResponse:
    # generate access_key and the room id
    # add new room in redis
    # set access_key  as key and room  id as value then store in redis
    # send back respone .
    pass
