# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: wmd.py
@time: 2017/3/10 9:51
@contact: ustb_liubo@qq.com
@annotation: query_sim :
"""
import sys
sys.path.append('/home/liubo-it/HotspotAnalysis/')
import logging
from logging.config import fileConfig
import os
from gensim.models import word2vec
from sklearn.metrics.pairwise import euclidean_distances
import pdb
import msgpack_numpy
from wmd.wmd import cal_sentence_distance
from time import time
import cPickle

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def load_all_query_keywords(keywords_file):
    query_keywords_dic = {}
    # {query:[(keyword, count), ..., (keyword, count)]}
    for line in open(keywords_file):
        tmp = line.rstrip().split('\t')
        if len(tmp) == 2:
            query = tmp[0]
            keywords = eval(tmp[1])
            query_keywords_dic[query] = keywords
    return query_keywords_dic


def load_all_address_query(address_query_file):
    address_query_dic = {}
    for line in open(address_query_file):
        tmp = eval(line.rstrip())
        if len(tmp) == 2:
            address_query_dic[tmp[0]] = tmp[1]
    return address_query_dic


def cal_query_distance(keyword_list1, keyword_list2, word2vec_model):
    '''
    :param keyword_list1: query1对应的keyword [(keyword, count), ..., (keyword, count)] 关键词和关键词出现的次数
    :param keyword_list2: query2对应的keyword
    :param word2vec_model
    :return:
    '''
    keyword_list1_vector, keyword_list1_freq = create_wmd_data(keyword_list1, word2vec_model)
    keyword_list2_vector, keyword_list2_freq = create_wmd_data(keyword_list2, word2vec_model)
    query_distance = \
        cal_sentence_distance(keyword_list1_vector, keyword_list1_freq, keyword_list2_vector, keyword_list2_freq)
    return query_distance


def create_wmd_data(keyword_list, word2vec_model):
    '''
        将query_search的结果转换成wmd的输入格式
    :param keyword_list:
    :param word2vec_model: word2vec模型 (用大规模语料库训练)
    :return:
    '''
    keyword_list_sum = sum(map(lambda x:x[1], keyword_list)) * 1.0
    keyword_list = map(lambda x:(x[0], x[1] / keyword_list_sum), keyword_list)
    keyword_list_vector = []
    keyword_list_freq = []
    for keyword_freq in keyword_list:
        keyword, freq = keyword_freq
        if keyword in word2vec_model:
            keyword_vector = word2vec_model[keyword]
            keyword_list_vector.append(keyword_vector)
            keyword_list_freq.append(freq)
    return keyword_list_vector, keyword_list_freq


if __name__ == '__main__':
    day = sys.argv[1]
    word2vec_model_path = '/data/liubo/hotspot/model/query_list_{}_country_wordcut.gensim.model'.format(day)
    word2vec_model = word2vec.Word2Vec.load(word2vec_model_path)

    # 每个城市的query
    address_query_dic = load_all_address_query(
        address_query_file='/data/liubo/hotspot/time_filter_f/time_filter_f_{}.txt'.format(day))
    # 每个query对应的keyword
    query_keywords_dic = load_all_query_keywords(
            keywords_file='/data/liubo/hotspot/query_search/keywords_{}_filter.txt'.format(day))
    # query_keywords_dic = load_all_query_keywords(
    #         keywords_file='/data/liubo/hotspot/query_search/keywords_recommend_20161130.txt')

    shanghai_1130_query_keyword_dic = {}

    # 得到每个query对应的search_result
    start = time()
    for address in address_query_dic:
        if '北京' in address:
            all_query = address_query_dic.get(address)[:200]
            for query in all_query:
                if query[0].encode('utf-8') in query_keywords_dic:
                    query_keyword = query_keywords_dic[query[0].encode('utf-8')]
                    if len(query_keyword) == 0:
                        continue
                    shanghai_1130_query_keyword_dic[query] = query_keyword
                    print query[0], '\t',
                    for t in query_keyword:
                        print t[0],
                    print
                else:
                    print 'not find query :', query
    print 'load time :', (time() - start)
    query_list = shanghai_1130_query_keyword_dic.keys()
    all_dist = []
    start1 = time()

    # # 用于输出数据, hadoop计算
    # new_dic = {}
    # for query in query_list:
    #     query_search_list = shanghai_1130_query_keyword_dic.get(query)
    #     keyword_list_vector, keyword_list_freq = create_wmd_data(query_search_list, word2vec_model)
    #     new_dic[query[0]] = (query_search_list, keyword_list_vector, keyword_list_freq)
    # cPickle.dump(new_dic, open('beijing_1130_query_keyword_dic.p', 'wb'))

    # 直接计算
    query_dist_dic = {}
    for index1, query1 in enumerate(query_list):
        for index2, query2 in enumerate(query_list):
            if index2 > index1:
                keyword_list1 = shanghai_1130_query_keyword_dic[query_list[index1]]
                keyword_list2 = shanghai_1130_query_keyword_dic[query_list[index2]]
                query_distance = cal_query_distance(keyword_list1, keyword_list2, word2vec_model)
                all_dist.append(query_distance)
                query_dist_dic[(query_list[index1][0], query_list[index2][0])] = query_distance
                # print index1, index2, query_distance
        print index1, (time() - start1)
        start1 = time()
    print len(all_dist)
    msgpack_numpy.dump((query_list, all_dist), open('/data/liubo/hotspot/query_search/all_query_dist_beijing_{}.p'.format(day), 'wb'))
    cPickle.dump(query_dist_dic, open('/data/liubo/hotspot/query_search/beijing_query_dist_dic_{}.p'.format(day), 'wb'))
    end = time()
    print 'time :', (end - start)
