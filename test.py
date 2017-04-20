# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: test.py
@time: 2017/2/28 18:25
@contact: ustb_liubo@qq.com
@annotation: test
"""
import sys
import logging
from logging.config import fileConfig
import os
import time
import datetime

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def get_day(current_day, day_diff):
    timeArray = time.strptime(current_day, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    threeDayAgo = dateArray - datetime.timedelta(days=day_diff)
    return threeDayAgo.strftime("%Y-%m-%d")

if __name__ == '__main__':
    current_day = '2017-03-09'
    for day_diff in range(1, 60):
        before_day = get_day(current_day, day_diff)
        code_dir = '/home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/query_search_cluster'
        command = 'sh %s/corpus.sh %s > %s/log/%s.txt &' %(code_dir, before_day, code_dir, before_day)
        print command



