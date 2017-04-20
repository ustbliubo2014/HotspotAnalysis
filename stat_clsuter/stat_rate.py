# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: stat_rate.py
@time: 2017/2/15 17:08
@contact: ustb_liubo@qq.com
@annotation: stat_rate
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
    all_count_file = 'brw_query_date.1d.20161101.csv'
    city_count_file = u'brw_query_date.1d.20161101_保定.csv'
    all_count_dic = {}  # {query:count}
    city_count_dic = {}   # {query:count}
    for line in open(all_count_file):
        tmp = line.rstrip().split('\t')
        if len(tmp) >= 3:
            count = int(tmp[0])
            query = tmp[1]
            all_count_dic[query] = all_count_dic.get(query, 0) + count
    for line in open(city_count_file):
        tmp = line.rstrip().split('\t')
        if len(tmp) >= 3:
            count = int(tmp[0])
            query = tmp[1]
            city_count_dic[query] = city_count_dic.get(query, 0) + count
    city_query_rate_dic = {}
    for query in city_count_dic:
        city_count = city_count_dic.get(query)
        all_count = all_count_dic.get(query)
        rate = city_count * 1.0 / all_count
        city_query_rate_dic[query] = rate
    items = city_query_rate_dic.items()
    items.sort(key=lambda x:x[1], reverse=True)
    for item in items:
        print item[0], item[1]
