# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: query_keyword.py
@time: 2017/4/11 15:04
@contact: ustb_liubo@qq.com
@annotation: query_keyword
"""
import sys
import logging
from logging.config import fileConfig
import os
import pdb
import cPickle

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def find_city_day():
    raw_file = '/data/liubo/hotspot/time_filter_f/time_filter_f_20161109.txt'
    query_keyword_file = '/data/liubo/hotspot/query_search/keywords_20161109_filter.txt'
    query_keyword_dic = {}
    country_20161109_query_keyword_dic = {}
    for line in open(query_keyword_file):
        tmp = line.rstrip().split('\t')
        if len(tmp) == 2:
            query = tmp[0].decode('utf-8')
            keyword_list = eval(tmp[1])
            query_keyword_dic[query] = keyword_list
    for line in open(raw_file):
        tmp = eval(line.rstrip())
        if len(tmp) == 2:
            query_list = tmp[1][:200]
            for query_item in query_list:
                query = query_item[0]
                if query in query_keyword_dic:
                    country_20161109_query_keyword_dic[query] = query_keyword_dic.get(query)
                else:
                    print query
    cPickle.dump(country_20161109_query_keyword_dic, open('/data/liubo/hotspot/yuqing/country_20161109_query_keyword_dic.p', 'wb'))


if __name__ == '__main__':
    # 得到query的keyword的信息 : [(keyword, freq)] [这里的freq和content中的tfidf作为权重, 用于向量求平均]
    # 取20161109中北京的query作为测试集
    pass
    find_city_day()
