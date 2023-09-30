import redis
import os

def connection_redis():
    pool_redis =redis.ConnectionPool(host=os.environ['REDIS_HOST'], password=os.environ['REDIS_PASSWORD'], port =6379)
    c_redis = redis.Redis(connection_pool=pool_redis)
    print("obteve conexão")
    return c_redis
