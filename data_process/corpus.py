# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: corpus.py
@time: 2017/3/10 14:23
@contact: ustb_liubo@qq.com
@annotation: corpus
"""
import sys
import logging
from logging.config import fileConfig
import os
import jieba
from util import stop_word_filter, chinese_word_filter, strQ2B
import traceback

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def mapper():
    for line in sys.stdin:
        try:
            dic = eval(line)
            content = dic.get('content', '')
            print '\t'.join(stop_word_filter([word for word in jieba.cut(chinese_word_filter(strQ2B(content)))]))
        except:
            traceback.print_exc()
            continue


if __name__ == '__main__':
    pass
    mapper()
