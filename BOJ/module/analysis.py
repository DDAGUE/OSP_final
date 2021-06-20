#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
from collections import Counter
from elasticsearch import Elasticsearch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

es_host = "127.0.0.1"
es_port = "9200"
es = Elasticsearch([{'host': es_host, 'port': es_port}], timeout=30)


def get_es_dna():
    party = dict()
    final = dict()
    res = es.get(index='movie', id=1)
    party = res['_source']
    new_list = party['director & actor'] + party['genre']
    final = {party['title'][0]: new_list}

    for i in range(2, 2001):
        res = es.get(index='movie', id=i)
        party = res['_source']
        new_list = party['director & actor'] + party['genre']
        final[party['title'][0]] = new_list

    return final


def get_cosine(vec1, vec2):  # 코사인 유사도값 반환 함수
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def list_to_vector(point):  # 주어진 리스트를 벡터화 시키는 함수
    return Counter(point)


def main_cosine(info):
    # 코사인 유사도 구하는 메인 함수,
    # 주어진 movie의 특징을 딕셔너리로 입력받음.
    # key값은 영화 이름, value값은 영화 특징들로 이뤄진 리스트 형태
    og_list = info
    og_v = list_to_vector(og_list)  # og_list를 벡터화한 값

    movie_2000 = get_es_dna()
    cos_2000 = dict()
    for key, value in movie_2000.items():
        cp_v = list_to_vector(value)
        cs = get_cosine(og_v, cp_v)
        cos_2000[key] = cs

    sort_2000 = sorted(cos_2000.items(), key=lambda x: x[1], reverse=True)

    return sort_2000[:10]


def get_es_story():
	party = dict()
	final = dict()
	res = es.get(index='movie',  id=1)
	party=res['_source']
	story_merge = str()
	for k in party['story']:
		story_merge = story_merge + k + " "
	final[party['title'][0]]=story_merge

	for i in range(2,2001):
		res = es.get(index='movie',  id=i)
		party=res['_source']
		story_merge = str()
		for k in party['story']:
			story_merge = story_merge + k + " "
		final[party['title'][0]]=story_merge

	return final



def list_to_dict(tfidfs):
	party=dict()
	final=dict()
	j=1
	res=es.get(index='movie',id=1)
	party=res['_source']
	final[party['title'][0]]=tfidfs[0]
	for i in range(2,len(tfidfs)+1):
		res=es.get(index='movie', id=i)
		party=res['_source']
		final[party['title'][0]]=tfidfs[j]
		j=j+1
	return final


def main_tfidf(story):
    # 분석 story parameter 넣어야함
    d = get_es_story() # dic 에서 story 추출하는 함수
    story_list = list(d.values())
    party = story
    # res = es.get(index='movie', id=21)
    # party = res['_source']
    mg = str()
    for k in party:
        mg = mg + k + " "
    og_story = mg
    story_list.append(og_story)

    tfidf_vect_simple = TfidfVectorizer()
    feature_vect_simple = tfidf_vect_simple.fit_transform(story_list)
    similarity_simple_pair = cosine_similarity(feature_vect_simple[-1:], feature_vect_simple)
    tfidf_cos_simil = similarity_simple_pair.tolist()
    tfitd_simil_list = sum(tfidf_cos_simil, [])
    del tfitd_simil_list[-1:]
    tfidf_cos_dict = list_to_dict(tfitd_simil_list)

    tfidf_sorted = sorted(tfidf_cos_dict.items(), key=lambda x: x[1], reverse=True)

    return tfidf_sorted[:10]

