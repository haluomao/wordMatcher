#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hot word cache based on redis.

Date: 2021-05-28
Author: maofagui
"""
import redis
from utils import singleton


@singleton
class RedisClient(object):
    """Redis client"""
    def __init__(self, host="127.0.0.1", port=6379):
        self._client = redis.Redis(host, port)

    def set(self, key, value):
        return self._client.set(key, value)

    def get(self, key):
        return self._client.get(key)

    def zadd(self, key, score, member, expire_sec=-1):
        # TODO (suxin520) impl it! You can see https://www.runoob.com/redis/redis-tutorial.html
        pass

    def zrange(self, key, start, stop, with_score=''):
        """ set with_score='WITHSCORES' if expect returning zrange with score"""
        # TODO (suxin520) impl it!
        pass


redis_cli = RedisClient(host="127.0.0.1", port=6379)


if __name__ == '__main__':
    redis_cli.set("a", "b")
    print(redis_cli.get('a'))
