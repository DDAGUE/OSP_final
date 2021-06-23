#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import requests
from flask import Flask
from flask import render_template
from flask import request
from module.Selected import make_info
from module.analysis import *


def call_API(words):
    api_movie = []
    idx = 0
    client_id = "sNhNY29KQ_9fggJH6kb4"
    client_key = "gN1zdMPlO2"
    movie = words
    url = f"https://openapi.naver.com/v1/search/movie.json?query={movie}"

    header = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_key
    }

    r = requests.get(url, headers=header)
    data = r.json()
    for info in data['items']:
        temp_t = re.sub('<b>', '', info['title'])
        temp_t = re.sub('</b>', '', temp_t)
        temp_d = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\$%&\\\=\(\'\"]', '. ', info['director'])
        temp_a = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\$%&\\\=\(\'\"]', '. ', info['actor'])
        api_info = {
            'idx': str(idx),
            'title': temp_t,
            'director': temp_d,
            'actor': temp_a,
            'image': info['image'],
            'link': info['link']
        }
        api_movie.append(api_info)
        idx = idx + 1
    return api_movie


app = Flask(__name__)


# 배열 넘겨줄때 방법을 찾아야함.
@app.route('/')
def home():
    if request.method == 'GET':
        return render_template('home.html')


@app.route('/result', methods=['GET', 'POST'])
def choice():
    menu = request.form['menu']
    tem = request.form['index']

    if menu == '배우, 감독, 장르가 비슷한 영화 찾기':
        return cosine(tem)
    elif menu == '줄거리가 비슷한 영화 찾기':
        return tf_idf(tem)


def tf_idf(index):
    tem = index

    movie_info = make_info(movie_list[int(tem)]['link'])

    temp_list = {
        'story': movie_info['story'],
    }
    middle = []
    for k in list(temp_list.values()):
        middle.extend(k)
    i = 1
    res = []
    temp = main_tfidf(middle)
    for k in temp:
        temp_dic = {
            'index': i,
            'title': k[0],
            'value': str(round(float(k[1]), 5))
        }
        res.append(temp_dic)
        i = i + 1

    return render_template('tfidf.html', res=res)


def cosine(index):
    tem = index
    # 선택한 영화 link 정보 parameter로 넘겨 정보 크롤링
    movie_info = make_info(movie_list[int(tem)]['link'])
    # ----- movie_info = {
    # -----    'title': Name,
    # -----    'genre': genre,
    # -----    'director & actor': d_a,
    # -----    'story': story
    # ----- }
    result_list = []
    temp_list = {
        'title': movie_info['title'],
        'genre': movie_info['genre'],
        'director & actor': movie_info['director & actor']
    }
    for k in list(temp_list.values()):
        result_list.extend(k)
    i = 1
    res = []
    temp = main_cosine(result_list)
    for k in temp:
        temp_dic = {
            'index': i,
            'title': k[0],
            'value': str(round(float(k[1]), 5))
        }
        res.append(temp_dic)
        i = i + 1

    return render_template('cosine.html', res=res)


@app.route('/movielist', methods=['GET', 'POST'])
def movielist():
    name = str()
    global movie_list
    if request.method == 'GET':
        name = request.args.get('title')
    movie_list = call_API(name)
    return render_template('movielist.html', items=movie_list)


if __name__ == "__main__":
    app.run()
