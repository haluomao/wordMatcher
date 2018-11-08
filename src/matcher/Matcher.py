#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Matcher, match keywords in word bags.

Date: 2018-10-29
Author: maofagui
"""
from src.model.WordBag import *


class Matcher(object):
    def __init__(self, word_bags):
        self.word_bags = word_bags

    def match_all(self, keywords):
        """
        match keywords with all word bags.

        :param keywords: keywords set, like set(['abc', 'def'])
        :return: a map of word bag name and intersection-set, like {'wordBagA': ['abc']}
        """
        res = {}
        for word_bag in self.word_bags:
            res.update(self.match(word_bag, keywords))
        return res

    def match_all_interrupt(self, keywords):
        """
        match keywords with all word bags, and interrupt when match one.

        :param keywords: keywords set, like set(['abc', 'def'])
        :return: a map of word bag name and intersection-set, like {'wordBagA': ['abc']}
        """
        res = {}
        for word_bag in self.word_bags:
            matched_res = self.match(word_bag, keywords)
            if len(matched_res[word_bag.name]):
                res.update(matched_res)
                return True, res
        return False, res

    @staticmethod
    def match(word_bag, keywords):
        """
        match by using set's intersection algorithm.

        :param word_bag: an instance of WordBag.
        :param keywords: keywords set, like set(['abc', 'def'])
        :return: a map of word bag name and intersection-set, like {'wordBagA': ['abc']}
        """
        return {word_bag.name: list(word_bag.data & keywords)}


if __name__ == '__main__':
    """
    An example.
    """
    data = {'abc', 'bcd', 'qwe'}
    bag = WordBag('wordBagA', data)
    keywords_set = {'abc', 'qwe', 'joke'}
    print(Matcher.match(bag, keywords_set))
