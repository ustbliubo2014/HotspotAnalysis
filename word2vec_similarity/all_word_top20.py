# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: all_word_top20.py
@time: 2017/2/10 11:37
@contact: ustb_liubo@qq.com
@annotation: all_word_top20
"""
import sys
import logging
from logging.config import fileConfig
import os
from sklearn.metrics.pairwise import cosine_similarity
from time import time
import pdb
import numpy as np

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    word_vector_list = []
    word_vector_file = '/data/liubo/wiki/wiki_word_vector.txt'
    count = 0
    start = time()
    for line in open(word_vector_file):
        count += 1
        tmp = line.split()
        word = tmp[0]
        vector = map(float, tmp[1:])
        word_vector_list.append((word, vector))
        if count == 100000:
            break
    print 'loaded'
    word_top20_sim = {}
    for element1 in word_vector_list:
        start = time()
        word1, vector1 = element1
        if len(vector1) != 200:
            continue
        all_sim = []
        count = 1
        for element2 in word_vector_list:
            if element1 == element2:
                continue
            word2, vector2 = element2
            if len(vector2) != 200:
                continue
            all_sim.append((word2, cosine_similarity(np.reshape(np.array(vector1), (1, 200)), np.reshape(np.array(vector2), (1, 200)))))
            if count % 10000 == 0:
                print count
            count += 1
        all_sim.sort(key=lambda x:x[1], reverse=True)
        end = time()
        print 'one word time :', end - start
