import redis

client = redis.StrictRedis("192.168.1.44",port=6379,db=0)