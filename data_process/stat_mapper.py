# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: stat_mapper.py
@time: 2017/2/14 18:07
@contact: ustb_liubo@qq.com
@annotation: stat_mapper
"""
import sys
import logging
from logging.config import fileConfig
import os

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def mapper(line):
    try:
        tmp = line.rstrip().split('\t')
        if len(tmp) > 6:
            query = tmp[4]
            if query.startswith('query'):
                query = query[9:]
                if len(query) < 40:
                    print '\t'.join([query, str(1)])
    except:
        # traceback.print_exc()
        return


if __name__ == '__main__':
    for line in sys.stdin:
        mapper(line)

