import json
import uuid

from fastapi import APIRouter, Depends

from crud.posts import create_post_in_db
from dependencies import get_current_user
from models.posts import PostCreate
from models.users import User
from redis_cache import get_redis_cache, FEED_CACHE_KEY_PATTERN
from utils.feeds import rebuild_feeds_for_users_friends, rebuild_feed

router = APIRouter(prefix='/v1')


@router.post("/posts/")
async def create_post(post: PostCreate,
                      current_user: User = Depends(get_current_user)):
    # TODO: чтобы избавится от эффекта леди гаги это нужно делать через очередь например
    #  с помощью celery. Тогда сможем контролировать rate limit и базе будет легче

    post_id: uuid.uuid4 = await create_post_in_db(current_user.id,
                                                  post.text)

    await rebuild_feeds_for_users_friends(current_user.id)

    return {"post_id": post_id}


@router.get("/posts/feed")
async def get_friends_feed(current_user: User = Depends(get_current_user)):
    cached_feed = get_redis_cache().get(
        FEED_CACHE_KEY_PATTERN.format(current_user.id)
    )
    if cached_feed:
        return json.loads(cached_feed)

    await rebuild_feed(current_user.id)

    cached_feed = get_redis_cache().get(
        FEED_CACHE_KEY_PATTERN.format(current_user.id)
    )
    return json.loads(cached_feed)

# TODO: реализовать оставшиеся методы
# @router.get("/post/")
# async def get_post():
#     pass
#
#
# @router.patch("/post/")
# async def update_post():
#     pass
#
#
# @router.delete("/post/")
# async def delete_post():
#     pass
