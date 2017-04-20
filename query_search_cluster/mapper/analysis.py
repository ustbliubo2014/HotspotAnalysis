# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: analysis.py
@time: 2017/3/28 9:47
@contact: ustb_liubo@qq.com
@annotation: analysis
"""
import sys
import logging
from logging.config import fileConfig
import os
import base64
import cPickle

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def analysis(content):
    (all_distance, query_dist_dic, query_list) = cPickle.loads(base64.b64decode(content))


if __name__ == '__main__':
    for line in sys.stdin:
        if len(line) < 100:
            continue
        analysis(line.rstrip())

