# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: analyse.py
@time: 2017/4/6 11:32
@contact: ustb_liubo@qq.com
@annotation: analyse
"""
import sys
sys.path.append('/home/liubo-it/HotspotAnalysis/')
import logging
from logging.config import fileConfig
import os
import cPickle
from query_search_cluster.query_sim import cal_sentence_distance
import pdb
from time import time

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    pass
    start = time()
    query_vector_freq_dic = cPickle.load(open('query_vector_freq_dic.p', 'rb'))
    url_vector_freq_dic = cPickle.load(open('url_vector_freq_dic.p', 'rb'))
    query_keyword_dic = cPickle.load(open('query_keyword_dic.p', 'rb'))
    url_keywords_dic = cPickle.load(open('url_keywords_dic.p', 'rb'))

    end = time()
    url = 'http://news.xinhuanet.com/yuqing/2015-01/09/c_127373707.htm'
    query = u'金五胖'
    query_vector_freq = query_vector_freq_dic.get(query)
    url_vector_freq = url_vector_freq_dic.get(url)
    query_keyword_list = query_keyword_dic.get(query)
    url_keyword_list = url_keywords_dic.get(url)
    print 'query_keyword_list :',
    for keyword in query_keyword_list:
        print keyword[0],
    print
    print 'url_keyword_list :',
    for keyword in url_keyword_list:
        print keyword[0],
    print
