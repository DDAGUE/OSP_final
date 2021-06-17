#!/usr/bin/python

import math
import re
from collections import Counter
from bs4 import BeautifulSoup
import requests

def get_cosine(vec1, vec2):i #코사인 유사도값 반환 함수
    intersection = set(vec1.keys()) & set(vec2.keys())
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


def main_cosine(origin): #코사인 유사도 구하는 메인 함수, 주어진 movie의 특징을 딕셔너리로 입력받음. key값은 영화 이름, value값은 영화 특징들로 이뤄진 리스트 형태
    og_list #원래 오리진 url에서 받아온 영화 특징으로 이뤄진 리스트
    og_v = list_to_vector(og_list) #og_list를 벡터화한 값

    movie_2000 = dict() #2000개의 영화를 저장할 딕셔너리, key값 : 영화 이름, value값 : 영화 특징 리스트
    cos_2000 = dict() #2000개의 영화의 코사인 유사도값 저장해둘 딕셔너리, key값 : 영화 이름, value값 : og와 비교한 코사인 유사도 값
    

    #만든 딕셔너리 정렬

    #탑10 리턴


    #구현해야 할 요소
    #1. 엘라스틱 서치에 입력된 영화 데이터들을 딕셔너리 형태로 끌어오기, {영화 이름:'영화 특징 리스트'}형태로 2000개 끌어오기.
    #2. {영화 이름:코사인 유사도 값}으로 딕셔너리 하나 더 생성, 나중에 유사도 값 정렬하고 비교하기 위함}
    #3. 기준 영화의 벡터값 기준으로 2000개 모두 비교, 딕셔너리 안에 코사인 유사도값 집어넣기
    #4. Top10 기준으로 정렬 후, 반환
