from fastapi import APIRouter

from auth import get_session, create_session, remove_session

router = APIRouter(prefix='/v1')


@router.post("/post/")
async def create_post():
    pass


@router.get("/post/")
async def get_post():
    pass


@router.patch("/post/")
async def update_post():
    pass


@router.delete("/post/")
async def delete_post():
    pass


@router.get("/post/feed")
async def get_friends_feed():
    pass
