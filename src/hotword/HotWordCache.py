#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hot word cache based on redis.

Date: 2021-05-28
Author: maofagui
"""
from enum import Enum
from RedisClient import redis_cli
import datetime


class TimeUnit(Enum):
    HOUR = 0
    DAY = 1


class HotWordCache(object):
    """
        Hot word cache.
        Use hourly slot to cache the the word and word's frequency.
        When getting the top list, merge hourly slot to final result.
    """

    def __init__(self, time_unit=TimeUnit.DAY, lifecycle=7, slot_name_prefix='slot'):
        self._time_unit = time_unit
        self._lifecycle = lifecycle
        self._slot_name_prefix = slot_name_prefix
        self._redis = redis_cli

    def incr(self, word, count=1):
        """increment the word's frequency"""
        return self._redis.zadd(self._cur_slot_name(), count, word, self._slot_expire_sec())

    def top(self, n=100, with_score=False):
        """get the top n word among lifecycle (the span until now)"""
        # TODO (suxin520) impl it!
        """
        Load word
        :return: top word
        """
        statistics_word_dic = {}
        word_top_list = []
        for all_slot_names in self._all_slot_names():
            for tup in self._redis.zrevrange(all_slot_names, 0, n, with_score=True):
                if tup[0] in statistics_word_dic:
                    statistics_word_dic[tup[0]] = statistics_word_dic[tup[0]] + tup[1]
                else:
                    statistics_word_dic[tup[0]] = tup[1]
        word_sort_list = sorted(statistics_word_dic.items(), key=lambda x: x[1], reverse=True)
        for hot_word, ranking in zip(word_sort_list, range(1, len(statistics_word_dic) + 1)):
            if with_score:
                word_top_list.append((hot_word[0].decode('utf-8'), ranking))
            else:
                word_top_list.append((hot_word[0].decode('utf-8'), int(statistics_word_dic[hot_word[0]]), ranking))
        return word_top_list

    def _slot_expire_sec(self):
        return self._lifecycle * 3600 * (24 if self._time_unit == TimeUnit.DAY else 1)

    def _cur_slot_name(self):
        """Get currenct slot name"""
        return self._slot_name_prefix + ':' + datetime.datetime.now().strftime('%Y%m%d-%H')

    def _all_slot_names(self):
        hours = self._lifecycle * (24 if self._time_unit == TimeUnit.DAY else 1)
        return [self._slot_name_prefix + ':' +
                (datetime.datetime.now() - datetime.timedelta(hours=delta)).strftime("%Y%m%d-%H")
                for delta in range(hours)]


if __name__ == '__main__':
    print(HotWordCache(slot_name_prefix='group')._all_slot_names())
    # print(HotWordCache(slot_name_prefix='group')._slot_expire_sec())
    print(HotWordCache(slot_name_prefix='group').incr("maofa", 1))
    print(HotWordCache(slot_name_prefix='group').top(with_score=False))
