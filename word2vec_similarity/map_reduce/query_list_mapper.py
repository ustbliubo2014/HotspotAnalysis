# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: query_list_mapper.py
@time: 2017/2/13 10:31
@contact: ustb_liubo@qq.com
@annotation: query_list_mapper
"""
import sys
import logging
from logging.config import fileConfig
import os
import traceback
import hashlib

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def mapper(line):
    try:
        tmp = line.decode('utf-8').rstrip().split('\t')
        if len(tmp) > 6:
            time = tmp[1][:10]
            ip = tmp[2]
            query = tmp[4]
            # m2 = hashlib.md5()
            # m2.update(ip)
            # ip = m2.hexdigest()

            # address = tmp[6]
            # address = address.split(',')
            # for k in range(len(address)-1, 0, -1):
            #     if len(address[k]) > 0:
            #         address = address[k]
            #         break
            if query.startswith('query'):
                query = query[9:]
                if len(query) < 40:
                    # print '\t'.join([ip, time, address, query])
                    print '\t'.join([ip, time, query])
    except:
        # traceback.print_exc()
        return


if __name__ == '__main__':
    for line in sys.stdin:
        mapper(line)
