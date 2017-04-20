# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: show.py
@time: 2017/4/13 11:58
@contact: ustb_liubo@qq.com
@annotation: show
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


if __name__ == '__main__':
    # test = []
    # for line in open('C:\Users\liubo\Desktop\country_result_score_20161124.txt'):
    #     tmp = eval(line.rstrip())
    #     if len(tmp) == 2:
    #         address = tmp[0]
    #         query = tmp[1]
    #         if '朝阳区' in address:
    #             for index, content in enumerate(query):
    #                 if content[1] == 11:
    #                     test.append(content)
    # pdb.set_trace()


    for line in open('/data/liubo/hotspot/time_filter_fd/time_filter_fd_20161124.txt'):
        tmp = eval(line.rstrip())
        if len(tmp) == 2:
            address = tmp[0]
            query_list = tmp[1]
            print len(query_list), len(set(query_list))
