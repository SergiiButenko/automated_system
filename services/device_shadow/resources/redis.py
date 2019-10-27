import redis
import os

Redis = redis.StrictRedis(
    host=os.environ["REDIS_LOCAL_HOST"],
    port=os.environ["REDIS_LOCAL_PORT"],
    db=0,
    decode_responses=True,
)
