# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: query_sim_mean.py
@time: 2017/4/13 14:57
@contact: ustb_liubo@qq.com
@annotation: query_sim_mean : 每个query的keyword对应的vector加权后取平均, 直接计算距离
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
import numpy as np

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
    keyword_mean_vector1 = create_mean_vector(keyword_list1, word2vec_model)
    keyword_mean_vector2 = create_mean_vector(keyword_list2, word2vec_model)
    query_distance = euclidean_distances(np.reshape(keyword_mean_vector1, (1, len(keyword_mean_vector1))),
                                         np.reshape(keyword_mean_vector2, (1, len(keyword_mean_vector2))))[0][0]
    return query_distance


def create_mean_vector(keyword_list, word2vec_model, vector_size=200):
    '''
        将query_search的keyword对应的向量加权求平均
    :param keyword_list:
    :param word2vec_model: word2vec模型 (用大规模语料库训练)
    :return:
    '''
    # keyword_list_sum = sum(map(lambda x:x[1], keyword_list)) * 1.0
    # keyword_list = map(lambda x:(x[0], x[1] / keyword_list_sum), keyword_list)
    keyword_mean_vector = np.asarray([0.0] * vector_size)
    find_num = 0
    for keyword_freq in keyword_list:
        keyword, freq = keyword_freq
        if keyword in word2vec_model:
            keyword_vector = word2vec_model[keyword]
            keyword_mean_vector += np.asarray(keyword_vector) * freq
            find_num += 1
    if find_num == 0:
        return None
    else:
        return keyword_mean_vector * 1.0 / find_num


if __name__ == '__main__':
    day = sys.argv[1]
    start = time()
    word2vec_model_path = '/data/liubo/hotspot/model/query_list_{}_country_wordcut.gensim.model'.format(day)
    word2vec_model = word2vec.Word2Vec.load(word2vec_model_path)
    end = time()
    print 'load word2vec_model_time :', (end - start)

    # 每个城市的query
    address_query_dic = load_all_address_query(
        address_query_file='/data/liubo/hotspot/time_filter_f/time_filter_f_{}.txt'.format(day))
    # 每个query对应的keyword
    query_keywords_dic = load_all_query_keywords(
            keywords_file='/data/liubo/hotspot/query_search/keywords_{}_filter.txt'.format(day))

    # 把所有的query一次聚类, 每个地区只取聚类结果就行
    country_1130_query_keyword_dic = {}

    # 得到每个query对应的search_result
    start = time()
    for address in address_query_dic:
        # if '北京' in address:
            all_query = address_query_dic.get(address)[:]
            for query in all_query:
                if query[0].encode('utf-8') in query_keywords_dic:
                    query_keyword = query_keywords_dic[query[0].encode('utf-8')]
                    if len(query_keyword) == 0:
                        continue
                    country_1130_query_keyword_dic[query] = query_keyword
                # else:
                #     print 'not find query :', query
    print 'load time :', (time() - start)
    query_list = country_1130_query_keyword_dic.keys()
    all_dist = []
    start1 = time()

    # 得到每个query的vector, 直接聚类
    all_query_vector = []
    real_query_list = []
    for index, query in enumerate(query_list):
        keyword_list = country_1130_query_keyword_dic[query]
        keyword_mean_vector = create_mean_vector(keyword_list, word2vec_model)
        if keyword_mean_vector != None:
            all_query_vector.append(keyword_mean_vector)
            real_query_list.append(query)
        else:
            print 'not find :', query
    all_query_vector = np.asarray(all_query_vector)
    msgpack_numpy.dump((real_query_list, all_query_vector), open('query_list-all_query_vector.p', 'wb'))

