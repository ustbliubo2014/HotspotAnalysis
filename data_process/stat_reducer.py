# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: stat_reducer.py
@time: 2017/2/14 18:07
@contact: ustb_liubo@qq.com
@annotation: stat_reducer
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
    last_query = ''
    last_query_count = 0
    for line in sys.stdin:
        try:
            tmp = line.strip().split('\t')
            if len(tmp) == 2:
                query = tmp[0]
                this_count = int(tmp[1])
                if query == last_query:
                    last_query_count += this_count
                    continue
                else:
                    print '\t'.join([last_query, str(last_query_count)])
                    last_query = query
                    last_query_count = this_count
                    continue
        except:
            # traceback.print_exc()
            continue
    try:
        print '\t'.join([last_query, str(last_query_count)])
    except:
        pass
