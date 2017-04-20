# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: tmp.py
@time: 2017/3/20 17:28
@contact: ustb_liubo@qq.com
@annotation: tmp
"""
import sys
import logging
from logging.config import fileConfig
import os
import cPickle

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    # day = sys.argv[1]
    # query_dist_dic = cPickle.load(open('/data/liubo/hotspot/query_search/beijing_query_dist_dic_{}.p'.format(day), 'rb'))
    # f_query_dist = open('/data/liubo/hotspot/query_search/beijing_query_dist{}.txt'.format(day), 'w')
    # for query in query_dist_dic:
    #     f_query_dist.write(query[0] + '\t'+ query[1] + '\t' + str(query_dist_dic.get(query)) + '\n')
    #     f_query_dist.write(query[1] + '\t'+ query[0] + '\t' + str(query_dist_dic.get(query)) + '\n')
    # f_query_dist.close()
    for index1 in range(10):
        query_list1 = range(10)
        for index2 in range(10):
            query_list2 = range(10)
            if index1 != index2:
                query_list1 = query_list1 + query_list2
        print index1, len(query_list1)