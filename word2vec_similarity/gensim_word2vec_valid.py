# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: gensim_word2vec_valid.py
@time: 2017/2/13 9:59
@contact: ustb_liubo@qq.com
@annotation: gensim_word2vec_valid
"""
import sys
import logging
from logging.config import fileConfig
import os
from gensim.models import word2vec
import logging

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    model = word2vec.Word2Vec.load(u"/data/liubo/wiki/wiki.zh.gensim.model")
    word5 = "美国".decode('utf-8')
    word4 = "中国".decode("utf-8")
    print model.similarity(word5, word4)
