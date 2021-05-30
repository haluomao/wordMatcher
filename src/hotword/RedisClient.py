#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hot word cache based on redis.

Date: 2021-05-28
Author: maofagui
"""
import redis
from wordMatcher.src.utils import singleton


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
        '''
        Load key ,word
        :return: word score
        '''
        # TODO (suxin520) impl it! You can see https://www.runoob.com/redis/redis-tutorial.html
        return self._client.zadd(key, {member: score}, nx=False, xx=False, ch=False, incr=True)

    def zrange(self, key, start, stop, with_score=''):
        """ set with_score='WITHSCORES' if expect returning zrange with score"""
        # TODO (suxin520) impl it!
        return self._client.zrange(key, start, stop, with_score='')

    def zrevrange(self, key, start, stop, with_score=''):
        """ set with_score='WITHSCORES' if expect returning zrange with score"""
        # https://blog.csdn.net/weixin_41201496/article/details/105187487
        # TODO (suxin520) impl it!
        '''
        :return: hot word sorting
        '''
        return self._client.zrevrange(key, start, stop, with_score)


redis_cli = RedisClient(host="127.0.0.1", port=6379)

if __name__ == '__main__':
    redis_cli.set("a", "b")
    print(redis_cli.get('a').decode('utf-8'))
    print(redis_cli.zrevrange('b', 0, 2))
    print(redis_cli.zadd('b', 1, str('ef')))
