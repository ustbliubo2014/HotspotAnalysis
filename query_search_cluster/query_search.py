# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: query_search.py
@time: 2017/3/7 17:11
@contact: ustb_liubo@qq.com
@annotation: query_search
"""
import sys
sys.path.append('/home/liubo-it/HotspotAnalysis/')
import logging
from logging.config import fileConfig
import os
from bs4 import BeautifulSoup
import urllib2
import traceback
from util.util import stop_word_filter, strQ2B, chinese_word_filter
import jieba
import pdb
from time import time

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')

query_num = 2000

def query_duplicated():
    day = sys.argv[1]
    query_file_name = '/data/liubo/hotspot/time_filter_fd/time_filter_fd_{}.txt'.format(day)
    f_result = open('/data/liubo/hotspot/query_search/unique_query_{}.txt'.format(day), 'w')
    query_dic = {}
    index = 0
    has_find_num = 0
    for line in open(query_file_name):
        try:
            address, all_query_score = eval(line)
            all_query_score = all_query_score[:query_num]
            all_query = map(lambda x: x[0], all_query_score)
            for query in all_query:
                if query not in query_dic:
                    query_dic[query] = 1
                    f_result.write(query + '\n')
                else:
                    has_find_num += 1
            index += 1
            print index, len(query_dic), has_find_num
        except:
            traceback.print_exc()
            continue


if __name__ == '__main__':
    pass
    query_duplicated()
