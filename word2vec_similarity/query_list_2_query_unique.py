# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: query_list_2_query_unique.py
@time: 2017/2/20 19:44
@contact: ustb_liubo@qq.com
@annotation: query_list_2_query_unique : 将query_list格式的数据转换成每行一个query的数据
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
    src_file = '/data/liubo/hotspot/query_list_beijing_20161109.txt'
    dst_file = '/data/liubo/hotspot/test_query_unique_beijing_20161109.txt'
    f_dst = open(dst_file, 'w')
    dic = {}
    count = 0
    for line in open(src_file):
        tmp = line.rstrip().split('\t')
        for k in tmp:
            if k in dic:
                continue
            else:
                dic[k] = 1
        count += 1
        if count % 100000 == 0:
            print count
    for k in dic:
        f_dst.write(str(k)+'\n')

