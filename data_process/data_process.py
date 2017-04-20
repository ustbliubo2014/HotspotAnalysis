# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: data_process.py
@time: 2017/2/15 15:41
@contact: ustb_liubo@qq.com
@annotation: data_process
"""
import sys
sys.path.insert('/home/liubo-it/HotspotAnalysis')
import logging
from logging.config import fileConfig
import os
from util.util import is_chinese_word
import jieba

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def num_trans(query):
    pass


def letter_process(query):
    # pm2.5, url, 特殊单词, 都不进行分词
    processed_words = []
    current_str = ''
    for word in query:
        if is_chinese_word(word):
            current_str = current_str + word
        else:
            if current_str != '':
                processed_words.append('\t'.join(list(jieba.cut(current_str.strip(), cut_all=False))))
                current_str = ''
                processed_words.append(word)
    processed_query = '\t'.join(processed_words)
    return processed_query


if __name__ == '__main__':
    pass
