# encoding=utf-8

import jieba
import jieba.analyse
from bs4 import BeautifulSoup
from collections import Counter
from pandas import DataFrame

def extract_post_content(file):
	soup = BeautifulSoup(open(file).read(), "html.parser")
	return soup.find('div', attrs={'class': 'entry-content'}).text
	
def fetch_feeds():
	return []

def extract_segments(data):
	seg_list = jieba.cut(data, cut_all=False)
	return [seg.strip() for seg in seg_list if len(seg) > 1]

def tokenize():	
	stoplist = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
	stoplist.extend(['...', 'com', 'using', u'使用', 'blog', u'博客', u'博客园', u'做法', u'论坛', 'part', u'部分', u'天下'])
	
	filtered = map(extract_segments, extract_all_text())

	tokens = Counter([word for words_in_article in filtered 
		for word in words_in_article 
		if word not in stoplist])

	return DataFrame(tokens.most_common(20), columns=['keywords', 'frequencies'])

# print(tokenize())

def extract_all_text():
	with open('filepaths') as f:
	    content = f.readlines()

	file_list = [x.strip() for x in content]
	return map(extract_post_content, file_list)

# print tokenize()


def taging(content):
	return ",".join(jieba.analyse.extract_tags(content, topK=32))

open('tags', "w").write("\n".join(map(taging, extract_all_text())).encode('utf-8'))
# for content in extract_all_text():
# 	tags = jieba.analyse.extract_tags(content, topK=32)
# 	print(",".join(tags))