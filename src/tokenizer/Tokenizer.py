#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tokenizer.

Date: 2018-10-29
Author: maofagui
"""


class Tokenizer:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def cut(self, text):
        return self.tokenizer.cut(text)
