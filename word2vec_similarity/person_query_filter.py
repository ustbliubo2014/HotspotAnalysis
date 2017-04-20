# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: person_query_filter.py
@time: 2017/2/20 12:09
@contact: ustb_liubo@qq.com
@annotation: person_query_filter : 先对同一个人的query进行过滤
"""
import sys
import logging
from logging.config import fileConfig
import os
from gensim.models import word2vec
import jieba
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from time import time

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    src_file = '/data/liubo/hotspot/query_list_beijing_20161101_utf8.txt'
    # 同一个人的, 先过滤
    dst_file = '/data/liubo/hotspot/query_person_filter_beijing_20161101_utf_8.txt'
    f_dst = open(dst_file, 'w')
    model_path = '/data/liubo/hotspot/test_query_uniq_beijing.gensim.model'
    model = word2vec.Word2Vec.load(model_path)
    filter_threshold = 0.8
    vector_length = 200
    all_person_all_query_count = 0
    filter_all_person_all_query_count = 0
    line_count = 0
    start = time()
    for line in open(src_file):
        all_query = line.rstrip().split('\t')
        all_query = list(set(all_query))
        all_query_vector = []
        for query in all_query:
            query = query.decode('utf-8')[:]
            this_vector = [0] * 200
            this_word_list = [word for word in jieba.cut(query, cut_all=False)]
            has_find = False
            for word in this_word_list:
                if word in model:
                    this_vector = this_vector + model[word]
                    has_find = True
            if has_find:
                this_vector = np.reshape(this_vector, (1, vector_length))
                all_query_vector.append((query, this_vector))

        if len(all_query_vector) > 0:
            write_query = [all_query_vector[0][0]]
            all_final_query_vector = [all_query_vector[0]]
            for this_element in all_query_vector[1:]:
                this_query, this_vector = this_element
                is_same = False
                for other_element in all_final_query_vector:
                    other_query, other_vector = other_element
                    if cosine_similarity(this_vector, other_vector) > filter_threshold:
                        is_same = True
                        # print 'same_query :', this_query, other_query
                        break
                    else:
                        continue
                if not is_same:
                    all_final_query_vector.append(this_element)
                    write_query.append(this_query)
            all_person_all_query_count += len(all_query_vector)
            filter_all_person_all_query_count += len(all_final_query_vector)
            f_dst.write('\t'.join(write_query)+'\n')
        line_count += 1
        if line_count % 1000 == 0:
            end = time()
            print line_count, all_person_all_query_count, filter_all_person_all_query_count, (end - start)
            start = time()
