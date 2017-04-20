# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: analysis.py
@time: 2017/2/15 18:54
@contact: ustb_liubo@qq.com
@annotation: analysis
"""
import sys
sys.path.insert('/home/liubo-it/HotspotAnalysis')
import logging
from logging.config import fileConfig
import os
import pdb
from time import time
from util.util import strQ2B

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    src_file = 'E:\git\HotspotAnalysis\data/query_city_20161130.txt'
    dst_file = 'E:\git\HotspotAnalysis\data/query_city_baoding_20161130.txt'
    f_dst = open(dst_file, 'w')
    last_ip = ''
    query_list = []
    ip_count = 0
    query_count = 0
    for line in open(src_file):
        tmp = line.rstrip().split('\t')
        if len(tmp) == 3:
            ip = tmp[0]
            this_time = int(tmp[1])
            query = tmp[2]
            query = strQ2B(query)
            if ip == last_ip:
                query_list.append((this_time, query))
            else:
                if len(query_list) > 0:
                    length = len(query_list)
                    query_count += length
                    print last_ip, length, query_count
                    query_list.sort(key=lambda x:x[0])
                    _last_time = query_list[0][0]
                    _last_query = query_list[0][1]
                    f_dst.write('\t'.join([last_ip, str(_last_time), _last_query])+'\n')
                    for _time, _query in query_list[1:]:
                        if abs(_time-_last_time) < 2 and _last_query == _query:
                            continue
                        else:
                            f_dst.write('\t'.join([last_ip, str(_time), _query])+'\n')
                            _last_time = _time
                            _last_query = _query
                last_ip = ip
                query_list = []
                query_list.append((this_time, query))
    if len(query_list) > 0:
        query_list.sort(key=lambda x: x[0])
        _last_time = query_list[0][0]
        _last_query = query_list[0][1]
        f_dst.write('\t'.join([last_ip, str(_last_time), _last_query]) + '\n')
        for _time, _query in query_list[1:]:
            if abs(_time - _last_time) < 2 and _last_query == _query:
                continue
            else:
                f_dst.write('\t'.join([last_ip, str(_time), _query]) + '\n')
                _last_time = _time
                _last_query = _query
        f_dst.close()

