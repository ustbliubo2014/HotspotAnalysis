# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: query_list_reducer.py
@time: 2017/2/13 10:31
@contact: ustb_liubo@qq.com
@annotation: query_list_reducer
"""
import sys
import logging
from logging.config import fileConfig
import os
import traceback
import jieba

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
                    last_query = query
                    last_time = time
                if ip == last_ip:
                    all_query.append((time, query))
                    continue
                else:
                    # 按时间排序
                    # all_query.sort(key=lambda x: x[0])
                    this_person_all_query = '\t'.join([x[1] for x in all_query])
                    print ' '.join([x for x in jieba.cut(this_person_all_query.strip(), cut_all=False)])
                    last_ip = ip
                    all_query = []
                    all_query.append((time, query))
                    continue
        except:
            # traceback.print_exc()
            continue
    try:
        # all_query.sort(key=lambda x: x[0])
        # print '\t'.join([x[1] for x in all_query])
        this_person_all_query = '\t'.join([x[1] for x in all_query])
        print ' '.join([x for x in jieba.cut(this_person_all_query.strip(), cut_all=False)])
    except:
        pass
