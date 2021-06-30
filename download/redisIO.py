#!/usr/bin/env python3

# step 1: import the redis-py client package
import redis, os

# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = os.environ['REDIS_HOST']
redis_port = 6379
redis_password = os.environ['REDIS_PASS']

redis_db0 = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True, db=0)
redis_db1 = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True, db=1)


def set_UserID(userID, filename):
    """Example Hello Redis Program"""
    # step 4: Set the hello message in Redis
    redis_db0.set(userID, filename)
    print("Redis (ID->Image) Set successful")     

def get_by_UserID(UserID):
    value = redis_db0.get(UserID)
    print("Filename get successful")
    return value

def set_filename(userID, filename):
    """Example Hello Redis Program"""
    # step 4: Set the hello message in Redis
    redis_db1.set(filename, userID)
    print("Redis (Image->ID) Set successful")     

def get_by_filename(filename):
    value = redis_db1.get(filename)
    print("UserIDs get successful")
    return value

def get_all_pairs():
    dic = {}
    for key in redis_db0.keys('*'):
        dic[key] = redis_db0.get(key)
    return dic

def get_all_filenames():
    files = []
    for key in redis_db0.keys('*'):
        files.append(redis_db0.get(key))
    return files
