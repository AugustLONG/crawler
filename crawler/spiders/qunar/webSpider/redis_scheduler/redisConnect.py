#-*-coding:utf-8-*-

import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_URL = None

def from_settings(settings):
    host = settings.get('REDIS_HOST',REDIS_HOST)
    port = settings.get('REDIS_PORT',REDIS_PORT)
    redis_url = settings.get('REDIS_URL',REDIS_URL)
    if redis_url:
        redis.from_url(redis_url)
    else:
        redis.Redis(host = host,port = int(port))

