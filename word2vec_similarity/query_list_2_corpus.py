# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: query_list_2_corpus.py
@time: 2017/2/20 11:12
@contact: ustb_liubo@qq.com
@annotation: query_list_2_corpus : 将query_list形式转换成语料的形式(分词)
"""
import sys
import logging
from logging.config import fileConfig
import os
import jieba
from time import time

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    #src_file = '/data/liubo/hotspot/query_list_20161110_country.txt'
    #dst_file = '/data/liubo/hotspot/query_list_20161110_country_wordcut.txt'
    src_file = sys.argv[1]
    dst_file = sys.argv[2]
    f_dst = open(dst_file, 'w')
    count = 0
    start = time()
    for line in open(src_file):
        try:
            line = line.decode('utf-8')
            f_dst.write(' '.join([x for x in jieba.cut(line.strip(), cut_all=False)])+'\n')
            count += 1
            if count % 50000 == 0:
                print count, (time() - start)
                start = time()
        except:
            continue
    f_dst.close()
