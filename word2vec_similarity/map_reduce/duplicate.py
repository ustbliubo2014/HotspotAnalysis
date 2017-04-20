# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: duplicate.py
@time: 2017/2/17 19:00
@contact: ustb_liubo@qq.com
@annotation: duplicate
"""
import sys
import logging
from logging.config import fileConfig
import os

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    raw_file = '/data/liubo/hotspot/test_query.txt'
    dst_file = '/data/liubo/hotspot/test_query_uniq.txt'
    f_dst = open(dst_file, 'w')
    dic = {}
    count = 0
    for line in open(raw_file):
        if line in dic:
            continue
        else:
            dic[line] = 1
            f_dst.write(line)
        count += 1
        if count % 100000 == 0:
            print count
    f_dst.close()
