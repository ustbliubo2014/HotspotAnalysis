# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: mapper_query_sim.py
@time: 2017/3/27 15:37
@contact: ustb_liubo@qq.com
@annotation: mapper_query_sim
"""
import sys
import logging
from logging.config import fileConfig
import os
import cPickle
import base64
from wmd import cal_sentence_distance
import pdb

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def cal_distance(city_query_keyword_dic):
    city_query_keyword_dic = {}
    query_list = city_query_keyword_dic.keys()
    all_distance = []
    query_dist_dic = {}
    for index1, query1 in enumerate(query_list):
        for index2, query2 in enumerate(query_list):
            if index2 > index1:
                query_search_list1, keyword_list_vector1, keyword_list_freq1 \
                    = city_query_keyword_dic[query_list[index1]]
                query_search_list2, keyword_list_vector2, keyword_list_freq2 \
                    = city_query_keyword_dic[query_list[index2]]
                query_distance = cal_sentence_distance(keyword_list_vector1, keyword_list_freq1, 
                                                       keyword_list_vector2, keyword_list_freq2)
                all_distance.append(query_distance)
                query_dist_dic[(query_list[index1], query_list[index2])] = query_distance
    return all_distance, query_dist_dic, query_list


if __name__ == '__main__':
    for line in sys.stdin:
        address, city_query_keyword_dic = cPickle.loads(base64.b64decode(line.rstrip()))
        all_distance, query_dist_dic, query_list = cal_distance(city_query_keyword_dic)
        print base64.b64encode(cPickle.dumps((address, all_distance, query_dist_dic)))
