# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: wmd.py
@time: 2017/3/13 15:09
@contact: ustb_liubo@qq.com
@annotation: wmd
"""
import sys
import logging
from logging.config import fileConfig
import os
from collections import namedtuple
from emd import emd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
import msgpack_numpy
import pdb
import math
from time import time

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def distance(f1, f2):
    # return euclidean_distances(np.reshape(f1, (1, len(f1))), np.reshape(f2, (1, len(f2))))[0][0]
    # start = time()
    tmp = math.sqrt(sum((a - b) ** 2 for a, b in zip(f1, f2)))
    # print 'cal one distance :', (time() - start)
    return tmp

def cal_sentence_distance(sentence1_word_vector_list, sentence1_word_freq_list,
                          sentence2_word_vector_list, sentence2_word_freq_list):
    start = time()
    sentence_distance = emd((sentence1_word_vector_list, sentence1_word_freq_list),
               (sentence2_word_vector_list, sentence2_word_freq_list),
               distance)
    end = time()
    # print 'cal time :', end - start
    return sentence_distance
    # features1 = [np.asarray([100, 40, 22]), np.asarray([211, 20, 2]), np.asarray([32, 190, 150]), np.asarray([2, 100, 100])]
    # weights1 = [0.8, 0.3, 0.2, 0.1]
    #
    # features2 = [np.asarray([100, 41, 26]), np.asarray([50, 100, 80]), np.asarray([255, 255, 255])]
    # weights2 = [0.5, 0.3, 0.2]
    #
    # print emd((features1, weights1), (features2, weights2), distance)


if __name__ == "__main__":
    pass