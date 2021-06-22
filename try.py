import redis, os

# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = os.environ['REDIS_HOST']
redis_port = 6379
redis_password = os.environ['REDIS_PASS']
redis_db0 = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True, db=0)

keys = redis_db0.keys('*')

for key in keys:
    print(redis_db0.get(key))
