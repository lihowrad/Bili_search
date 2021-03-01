# -*- coding: utf-8 -*-
import pandas as pd
import jieba
import jieba.analyse as analyse
import re

jieba_done = 'result_keywords.csv'
data = pd.read_csv('result.csv', header=None, names=['content', 'time', 'UID'])
data_txt = re.sub(r'\W*', '', ''.join(list(data.iloc[1:-1, 0])))
word_list = ' '.join(jieba.cut(data_txt, cut_all=False))
keywords = jieba.analyse.extract_tags(word_list, topK=20, withWeight=True, allowPOS=())
keywords_list = []
freq = []
for set_tmp in keywords:
    freq.append(set_tmp[1])
    keywords_list.append(set_tmp[0])
data_done = pd.DataFrame({'高频词': keywords_list, '出现频率': freq})
data_done.to_csv(jieba_done, index=False)