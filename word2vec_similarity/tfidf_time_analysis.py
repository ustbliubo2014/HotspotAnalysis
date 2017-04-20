# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: tfidf_time_analysis.py
@time: 2017/2/22 16:21
@contact: ustb_liubo@qq.com
@annotation: tfidf_time_analysis
"""
import sys
import logging
from logging.config import fileConfig
import os
import pdb

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    path = '/data/liubo/hotspot/all_city_20161107.txt'
    dst_file = '/data/liubo/hotspot/beijing_query_top10000_20161107.txt'
    f_dst = open(dst_file, 'w')
    city_name = '北京'.decode('utf-8')
    for line in open(path):
        line = eval(line)
        if city_name in line[0]:
            for k in line[1]:
                query, score, count = k
                f_dst.write(str(query)+'\n')
    f_dst.close()
