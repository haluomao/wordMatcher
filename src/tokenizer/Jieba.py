#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Encapsulated Jieba APIs.

Date: 2018-10-29
Author: maofagui
"""
import jieba
jieba.initialize()


class Jieba(object):
    def __init__(self, conf=None):
        self.cut_all = False
        if conf and conf['mode'] == 'full':
            self.cut_all = True

    def cut(self, text):
        """
        cut text with precision as default.
        """
        return self.cut_precision(text)

    def cut_full_mode(self, text):
        """
        cut with full mode. (cut_all = True)
        """
        return jieba.cut(text, cut_all=self.cut_all)

    def cut_precision(self, text):
        """
        cut with precision mode. (cut_all = False)
        """
        return jieba.cut(text, cut_all=self.cut_all)

    def cut_for_search(self, text):
        """
        cut for search
        """
        return jieba.cut_for_search(text)


print('Loaded Jieba.py.')

if __name__ == '__main__':
    list0 = jieba.cut('小明硕士毕业于某所大学，后来在某处勤奋地编代码', cut_all=True)
    print('全模式', list(list0))
