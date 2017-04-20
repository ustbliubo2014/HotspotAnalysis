# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: tmp.py
@time: 2017/2/15 16:20
@contact: ustb_liubo@qq.com
@annotation: tmp
"""
import sys
import logging
from logging.config import fileConfig
import os
import pdb

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


for line in open('tfidf_time_1101.txt'):
    tmp = eval(line)
    if u"保定" in tmp[0]:
        address = tmp[0].split('\t')[0]
        for key in tmp[1]:
            print address, key[0], key[1]

