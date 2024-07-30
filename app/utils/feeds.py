import json
import uuid


from crud.posts import get_feeds_posts
from crud.users import get_followers
from models.posts import Post
from redis_cache import get_redis_cache, FEED_CACHE_KEY_PATTERN


async def rebuild_feed(user_id):
    posts: list[Post] = await get_feeds_posts(user_id)

    await get_redis_cache().set(
        FEED_CACHE_KEY_PATTERN.format(user_id),
        json.dumps([post.dict() for post in posts])
    )


async def rebuild_feeds_for_users_friends(user_id: uuid.uuid4()):
    """Пересобираем ленты тех кто подписан на пользователя."""

    followers_ids = await get_followers(user_id)

    for _id in followers_ids:
        await rebuild_feed(_id)
