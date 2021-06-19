#!/usr/bin/python3
#-*- coding: utf-8 -*-

import requests
import math
from collections import Counter
from bs4 import BeautifulSoup
import re
import sys
from elasticsearch import Elasticsearch


es_host="127.0.0.1"
es_port="9200"
es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)


def get_esdata():
	party = dict()
	final = dict()
	res = es.get(index='movie',  id=1)
	party=res['_source']
	new_list = party['director & actor'] + party['genre']
	final={party['title'][0] : new_list}

	for i in range(2,2001):
		res = es.get(index='movie',  id=i)
		party=res['_source']
		new_list = party['director & actor'] + party['genre']
		final[party['title'][0]]=new_list
	return final


def get_cosine(vec1, vec2): #코사인 유사도값 반환 함수
	intersection=set(vec1.keys())&set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])

	sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
	sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)

	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator


def list_to_vector(point):#주어진 리스트를 벡터화 시키는 함수
	return Counter(point)


def main_cosine(): #코사인 유사도 구하는 메인 함수, 주어진 movie의 특징을 딕셔너리로 입력받음. key값은 영화 이름, value값은 영화 특징들로 이뤄진 리스트 형태
	og_list =['드라마','스티브 맥퀸','마이클 패스벤더','캐리 멀리건','제임스 뱃지 데일']
	og_v = list_to_vector(og_list) #og_list를 벡터화한 값

	movie_2000=get_esdata()
	cos_2000 = dict()
	for key,value in movie_2000.items() :
		cp_v=list_to_vector(value)
		cs=get_cosine(og_v,cp_v)
		cos_2000[key]=cs

	sort_2000=sorted(cos_2000.items(), key=lambda x: x[1], reverse=True)
	
	print(sort_2000[:10])
	

if __name__ == "__main__":
	main_cosine()
