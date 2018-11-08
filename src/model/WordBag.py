#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Word bag model.

Date: 2018-10-29
Author: maofagui
"""


class WordBag(object):
    def __init__(self, name, data=None):
        """
        init word bag.

        :param name: string
        :param data: set
        """
        self.name = name
        self.data = data
