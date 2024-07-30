import os

import redis

from dotenv import load_dotenv

load_dotenv()

FEED_CACHE_KEY_PATTERN = 'feed:{}'


redis_cache = redis.from_url(f"redis://{os.getenv('REDIS_CACHE_HOST')}:{os.getenv('REDIS_CACHE_PORT')}",
                             encoding="utf8",
                             decode_responses=True)


def get_redis_cache():
    return redis_cache
