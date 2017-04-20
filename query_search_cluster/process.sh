#!/bin/bash

today=$1
echo $today
python /home/liubo-it/HotspotAnalysis/query_search_cluster/query_search.py  $today
python /home/liubo-it/HotspotAnalysis/query_search_cluster/mapper_query_search.py $today
python /home/liubo-it/HotspotAnalysis/query_search_cluster/reducer_query_search.py $today

