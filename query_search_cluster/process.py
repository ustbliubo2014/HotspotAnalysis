# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: process.py
@time: 2017/4/10 11:38
@contact: ustb_liubo@qq.com
@annotation: process
"""
import sys
import logging
from logging.config import fileConfig
import os
import time
import commands
from scp_file import scp_remote2local, scp_local2remote, exec_remote_command
import datetime

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def get_yesterday(day):
    timeArray = time.strptime(day, "%Y%m%d")
    timeStamp = int(time.mktime(timeArray))
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    yesterday = dateArray - datetime.timedelta(days=1)
    yesterday = yesterday.strftime("%Y%m%d")
    return yesterday


if __name__ == '__main__':
    day = sys.argv[1]
    yesterday = get_yesterday(day)
    print day, yesterday

    # 格式转换
    timeArray = time.strptime(day, "%Y%m%d")
    day_other_format = time.strftime("%Y-%m-%d", timeArray)

    # 获取数据
    cmd = 'hadoop fs -text /home/hdp-skyeye/proj/hdp-skyeye-algorithm/lining-s/tfidf_time/time_filter_fd_{}/part* > ' \
          '/home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/time_filter_fd/time_filter_fd_{}.txt'.format(day_other_format, day)
    commands.getoutput(cmd)
    print 'finish download file'

    # 将数据拷贝到dpl07
    scp_local2remote(ip='dpl07.skyeyes.lycc.qihoo.net', user='liubo-it', passwd='qwer1234!@#$QWER',
                     dst_path='/data/liubo/hotspot/time_filter_fd',
                     filename='/home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/time_filter_fd/time_filter_fd_{}.txt'.format(day))

    # 在dpl07上执行命令(转换成hadoop格式)
    start = time.time()
    command = 'sh /home/liubo-it/HotspotAnalysis/query_search_cluster/process.sh {}'.format(day)
    exec_remote_command(ip='dpl07.skyeyes.lycc.qihoo.net', port=22, user='liubo-it', password='qwer1234!@#$QWER', command=command)
    end = time.time()
    print 'dpl07_time :', (end - start)

    # 将dpl07上的数据拷贝到hadoop
    start = time.time()
    scp_remote2local(ip='dpl07.skyeyes.lycc.qihoo.net', user='liubo-it', passwd='qwer1234!@#$QWER',
                     local_path='/home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/hadoop_file',
                     remote_path='/data/liubo/hotspot/hadoop_file/{}.tgz'.format(day), is_folder=False)
    cmd = 'cd /home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/hadoop_file; ' \
          'tar -xvf /home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/hadoop_file/{}.tgz '.format(day)
    commands.getoutput(cmd)
    cmd = 'mv /home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/hadoop_file/data/liubo/hotspot/hadoop_file/{} ' \
          '/home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/hadoop_file/'.format(day)
    commands.getoutput(cmd)

    # 数据上传到hdfs
    cmd = 'hadoop fs -rmr /home/hdp-skyeye-algorithm/liubo-it/query_cluster_district/wmd_hadoop/hadoop_file/{}'.format(day)
    commands.getoutput(cmd)
    cmd = 'hadoop fs -put  /home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/hadoop_file/{}  ' \
          '/home/hdp-skyeye-algorithm/liubo-it/query_cluster_district/wmd_hadoop/hadoop_file/'.format(day)
    commands.getoutput(cmd)
    cmd = 'rm -rf /home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/hadoop_file/{}*'.format(day)
    commands.getoutput(cmd)
    end = time.time()
    print 'dpl07-hdfs_time :', (end - start)

    # # 执行mr, 聚类
    start = time.time()
    cmd = 'sh /home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/query_search_cluster/mapper/query_sim_district.sh {}'.format(day)
    commands.getoutput(cmd)
    end = time.time()
    print 'cluster_time :', (end - start)

