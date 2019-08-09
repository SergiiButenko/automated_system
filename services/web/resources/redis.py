import redis
import os

redis = redis.StrictRedis(
    host=os.environ["REDIS_HOST"],
    port=os.environ["REDIS_PORT"],
    db=0,
    decode_responses=True,
)
