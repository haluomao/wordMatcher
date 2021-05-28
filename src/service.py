#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
App booter.

Date: 2018-10-31
Author: maofagui
"""

from flask import Flask
from flask import jsonify
from flask import request
import urllib.request
import yaml
import logging
from logging.handlers import TimedRotatingFileHandler

from model.WordBag import WordBag
from matcher.Matcher import Matcher
from tokenizer.Tokenizer import Tokenizer

ROOT_PATH = '../'

app = Flask(__name__)
handler = TimedRotatingFileHandler(ROOT_PATH + '/log/word-matcher.log')
formatter = logging.Formatter(
    "%(asctime)s %(processName)s %(threadName)s [%(filename)s:%(lineno)d %(funcName)s] %(levelname)s %(message)s",
    "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)
# app.logger.setLevel(logging.INFO)

yml_config = yaml.load(open(ROOT_PATH + '/conf/config.yml', 'r'))


def parse_content(path, path_type):
    if path_type == 'url':
        with urllib.request.urlopen(path) as file:
            content = file.read().decode('utf-8')
    else:
        with open(ROOT_PATH + path, 'r') as file:
            content = file.read()
    return set(content.splitlines())


def load_tokenizer():
    """
    Load tokenizer.
    :return: a tokenizer
    """
    app.logger.info("loading tokenizer...")
    tokenizer_conf = 'Jieba'
    if 'tokenizer' in yml_config.keys():
        tokenizer_conf = yml_config['tokenizer']
    module = __import__('tokenizer.' + tokenizer_conf)
    clazz = getattr(getattr(module, tokenizer_conf), tokenizer_conf)
    obj = clazz(yml_config[tokenizer_conf])
    app.logger.info("loaded tokenizer: %s", tokenizer_conf)
    runnable=1
    return Tokenizer(obj)


def load_word_bags():
    """
    Reload word bags.

    :return: word bag list.
    """
    app.logger.info("loading word bag...")
    word_bags_list = []
    for word_bag_conf in yml_config['word_bags']:
        content = parse_content(word_bag_conf['content'], word_bag_conf['type'])
        app.logger.debug("name:%s, content:%s", word_bag_conf['name'], content)
        word_bags_list.append(WordBag(word_bag_conf['name'], content))
        app.logger.info("loaded word bag: %s", word_bag_conf['name'])
    return word_bags_list
    # dir_path = '/Users/maofagui/system_invisible'
    # paths = os.listdir(dir_path)
    # for path in paths:
    #     print(path)
    #     if not path.endswith('.json'):
    #         continue
    #     with open(dir_path + '/' + path, 'r') as file:
    #         load_dict = json.load(file)
    #         word_bags_list.append(WordBag(path, {item['content'] for item in load_dict['contents']}))
    # return word_bags_list


tokenizer = load_tokenizer()
word_bags = load_word_bags()
matcher = Matcher(word_bags)


@app.route('/reload', methods=['PUT'])
def reload():
    """
    reload tokenizer and word bags.
    :return: void
    """
    app.logger.info("reloading tokenizer, word bags, and matcher.")
    global tokenizer
    global word_bags
    global matcher
    try:
        tokenizer = load_tokenizer()
        word_bags = load_word_bags()
        matcher = Matcher(word_bags)
        app.logger.info("reloaded successfully.")
        return jsonify({
            'status': 'success',
            'message': 'reload done.'
        }), 200
    except Exception as e:
        app.logger.error("reload error.")
        return jsonify({
            'status': 'success',
            'code': 'InternalServerError',
            'message': str(e)
        }), 500


@app.route('/match', methods=['POST'])
def match():
    """
    input json:
    {
        "text": "The quick brown fox jumps over a lazy dog."
    }
    """
    request_body = ''
    try:
        request_body = request.json
        app.logger.info("Request.json: %s", request_body)
        text = request_body['text']
        keywords = set(tokenizer.cut(text))
        app.logger.debug("keywords:%s", keywords)
        res = matcher.match_all(keywords)
        app.logger.debug("res:%s", res)
        return jsonify({
            'status': 'success',
            'data': res
        }), 200
    except Exception as e:
        app.logger.error("result for (%s) is: %s", request_body, 'failed with message' + str(e))
        return jsonify({
            'status': 'failed',
            'code': 'InternalServerError',
            'message': str(e)
        }), 500


@app.route('/', methods=['GET', 'POST'])
def check_worker_alive():
    """
    checking whether a worker is alive
    :return: a message.
    """
    app.logger.info("come in successfully.")
    return jsonify({
        'status': 'success',
        'message': 'I am Ok!'
    }), 200


if __name__ == '__main__':
    app.run(yml_config['app']['host'], yml_config['app']['port'])
