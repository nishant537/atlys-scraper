import redis
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST") 
REDIS_PORT = os.getenv("REDIS_PORT")

class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        # clearing all the cache on application initialisation
        self.redis_client.flushdb()

    def get_cached_price(self, product_title):
        return self.redis_client.get(product_title)

    def cache_price(self, product_title, price):
        self.redis_client.set(product_title, price)
