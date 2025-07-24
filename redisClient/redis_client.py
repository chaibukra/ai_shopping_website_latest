import redis

from config.config import Config

config = Config()
redis_client = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT,password=config.REDIS_PASSWORD, username=config.REDIS_USERNAME, decode_responses=True, ssl=config.REDIS_SSL)
