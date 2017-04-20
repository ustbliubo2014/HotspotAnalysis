# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: query_list_combiner.py
@time: 2017/2/24 16:25
@contact: ustb_liubo@qq.com
@annotation: query_list_combiner
"""
import sys
import logging
from logging.config import fileConfig
import os

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    all_query = []
    last_ip = ''
    last_time = ''
    last_query = ''
    for line in sys.stdin:
        try:
            tmp = line.strip().split('\t')
            if len(tmp) == 3:
                ip = tmp[0]
                time = float(tmp[1])
                query = tmp[2]
                if time == last_time and last_query == query:
                    continue
                else:
                    print line.rstrip()
        except:
            # traceback.print_exc()
            continue
