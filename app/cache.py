import redis
import json

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def get_cached_products():
    data = redis_client.get("products")
    if data:
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return None
    return None

def set_cached_products(products):
    try:
        redis_client.set("products", json.dumps(products), ex=300)  # cache for 5 minutes
    except Exception as e:
        print("Redis cache error:", e)

def clear_cached_products():
    redis_client.delete("products")
