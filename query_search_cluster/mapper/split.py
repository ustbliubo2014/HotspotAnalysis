# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: split.py
@time: 2017/3/28 12:27
@contact: ustb_liubo@qq.com
@annotation: split
"""
import sys
import logging
from logging.config import fileConfig
import os
import base64
import cPickle
import pdb

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':

    src_folder = '/home/liubo-it/hadoop_file/'
    dst_folder = '/home/hdp-skyeye-algorithm/hadoop_file_split/'
    day_list = os.listdir(src_folder)
    for day in day_list:
        day_src_folder = os.path.join(src_folder, day)
        day_dst_folder = os.path.join(dst_folder, day)
        if not os.path.exists(day_dst_folder):
            os.makedirs(day_dst_folder)
        file_list = os.listdir(day_src_folder)
        for file_name in file_list:
            dst_file_name = os.path.join(day_dst_folder, file_name)
            src_file_name = os.path.join(day_src_folder, file_name)
            content = open(src_file_name).read().rstrip()
            address, new_dic = cPickle.loads(base64.b64decode(content))
            print address
            f = open(dst_file_name, 'w')
            for query in new_dic:
                f.write(base64.b64encode(cPickle.dumps((address, query, new_dic.get(query))))+'\n')
            f.close()