#-*- coding: utf-8 -*-
__author__ = 'liubo-it'

import os
import sys

# 将一些常用参数放在conf中,修改时方便

# 存放message数据的文件夹
data_folder = '/data/liubo/liubo_data/message/'

# 一种类型的数据建立一个文件夹,这样数据不容易乱
# child_folder = 'first_class'
# child_folder = 'fraud_second_class'
# child_folder = 'illegal_second_class'
# child_folder = 'promote_second_class'
child_folder = 'first_second_class'

data_folder = os.path.join(data_folder, child_folder)
if not os.path.exists(data_folder):
    os.mkdir(data_folder)

# 用所有数据训练的word2vec (可以先进行数据处理,然后在训练word2vec)
all_chinese_word2vec_file = 'content_topic_000000_0_30_duplicate_chinese_word_vector.txt'

# word2vec的执行文件的path
word2vec_exe_path = '/home/liubo-it/word2vec/word2vec'
vector_length = 200

# 由于已经为每种数据建立了单独的文件夹,所以文件名中就不用带具体数据的名字了
# 原始的content_label文件
raw_content_label_file = os.path.join(data_folder, 'content_label.txt')
# 处理后的content_label文件
content_label_file = os.path.join(data_folder, 'preProcess_content_label.txt')
# 分词后的content,用于word2vec训练
content_word_cut_file = os.path.join(data_folder, 'preProcess_content_cut_word.txt')
# content生成的词向量
content_word_vector_file = os.path.join(data_folder, 'preProcess_content_word_vector.txt')
# label content vector
content_vector_label_file = os.path.join(data_folder, 'preProcess_content_vector_label.txt')
# 将label转换成数字
label_trans_file = os.path.join(data_folder, 'label_trans_file.p')
# 训练好的模型文件
model_file = os.path.join(data_folder, 'model.p')
all_word_file = os.path.join(data_folder, 'all_word.p')
# 每个词的权重 -- tf-idf
word_weight_file = os.path.join(data_folder, 'word_weight.p')
# 特征选择后的词
word_select_file = os.path.join(data_folder, 'word_select.p')
sentence_numpy_file = os.path.join(data_folder, 'sentence_numpy.p')
word_idf_file = os.path.join(data_folder, 'word_idf_dic.p')
content_weight_vector_label_file = os.path.join(data_folder, 'preProcess_content_weight_vector_label.txt')

train_data_file = os.path.join(data_folder, 'train_data.p')
valid_data_file = os.path.join(data_folder, 'valid_data.p')
valid_content_file = os.path.join(data_folder, 'valid_content.p')

url_file = os.path.join(data_folder, 'all_train_url.txt')
url_type_file = os.path.join(data_folder, 'all_train_url_type.txt')
url_type_dic_file = os.path.join(data_folder, 'all_train_url_type_dic.p')
contentIndex_urlType_dic_file = os.path.join(data_folder, 'contentIndex_urlType_dic.p')

binary_classify_folder = os.path.join(data_folder, 'binary_classify')

# 每个类取多少个关键词
topK = 20
topK_file = os.path.join(data_folder, 'topK.p')

# cnn lstm 中可能用到的变量
cnn_lstm_max_length = 20
max_features = 20000
skip_top = 0
batch_size = 32
epoch_num = 3
word_index_dic_file = os.path.join('/home/data/liubo/message/first_class', 'dnn_word_index_dic.p')
# 将矩阵转换成numpy矩阵存储
content_numpy_data_label_file = os.path.join(data_folder, 'preProcess_content_numpy_data_label.p')
content_cut_label_file = os.path.join(data_folder, 'preProcess_content_cut_label_file.p')

