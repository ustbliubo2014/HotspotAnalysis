# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: query_list_address.py
@time: 2017/2/14 14:15
@contact: ustb_liubo@qq.com
@annotation: query_list_address
"""
import sys
import logging
from logging.config import fileConfig
import os

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def address_split(raw_file, dst_folder):
    # 将全部数据按地点分成多个文件[放在dst_folder下](一个地点一个文件)
    for line in open(raw_file):
        pass


if __name__ == '__main__':
    pass
