# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: data_filter.py
@time: 2017/2/13 14:26
@contact: ustb_liubo@qq.com
@annotation: data_filter : 过滤不能处理的字符
"""
import sys
import logging
from logging.config import fileConfig
import os
import msgpack_numpy

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def utf8_filter():
    f_new = open(sys.argv[2], 'w')
    count = 1
    for line in open(sys.argv[1]):
        try:
            line = line.decode('utf-8').rstrip()
            f_new.write(line+'\n')
        except:
            continue
        if count % 100000 == 0:
            print count
        count += 1
    f_new.close()


def query_length_filter():
    # 一个ip查询次数少于5, 过滤掉
    f_new = open('/data/liubo/hotspot/query_list_length_filter.txt', 'w')
    count = 1
    for line in open('/data/liubo/hotspot/query_list_20161130_new.txt'):
        try:
            tmp = line.rstrip().split('\t')
            if len(tmp) < 6:
                continue
            f_new.write(line+'\n')
        except:
            continue
        if count % 100000 == 0:
            print count
        count += 1
    f_new.close()


def word_length_stat():
    # 每个查询词的长度不超过30
    word_dic = msgpack_numpy.load(open('/data/liubo/hotspot/all_query_dic.p', 'rb'))
    word_length_dic = {}
    for word in word_dic:
        word_length = len(word)
        word_length_dic[word_length] = word_length_dic.get(word_length, 0) + 1
    print word_length_dic


def address_filter():
    filter_address = "保定"
    raw_file = '/data/liubo/hotspot/query_list_address_20161130.txt'
    dst_file = '/data/liubo/hotspot/query_list_{}_20161130.txt'.format(filter_address)
    f_dst = open(dst_file, 'w')
    for line in open(raw_file):
        tmp = line.rstrip().split('\t')
        if len(tmp) > 2:
            address = tmp[0]
            if address == filter_address:
                f_dst.write('\t'.join(tmp[1:])+'\n')
    f_dst.close()


def decode_filter(raw_file, dst_file):
    # 过滤编码错误的
    all_lines = []
    for line in open(raw_file):
        tmp = line.encode('utf-8').rstrip().split()
        if len(tmp) < 5:
            continue
        all_lines.append(line)
    all_lengths = len(all_lines)
    f_dst = open(dst_file, 'w')
    for line in all_lines[int(all_lengths*0.2):]:
        f_dst.write(line)
    f_dst.close()



if __name__ == '__main__':
    pass

    # utf8_filter()
    # query_length_filter()
    # word_length_stat()
    # address_filter()
