#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import requests
import json
from flask import Flask
from flask import render_template
from flask import request

def call_API(words):

	api_movie = []
	idx = 1
	client_id = "sNhNY29KQ_9fggJH6kb4"
	client_key = "gN1zdMPlO2"
	movie = words
	url = f"https://openapi.naver.com/v1/search/movie.json?query={movie}"

	header = {
		"X-Naver-Client-Id" : client_id,
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

@app.route('/tfidf', methods=['GET', 'POST'])
def tf_idf():
	tf = ''
	tf = {1:'park', 2:'jung', 3:'kang'}
	return render_template('tfidf.html', result=tf)

@app.route('/cosine', methods=['GET', 'POST'])
def cosine():
	cos = ''
	cos = {1:'park', 2:'jung', 3:'kang'}
	tem = str()
	if request.method == 'GET':
		tem = request.args.get('index')
	return render_template('cosine.html', res=tem)

@app.route('/movielist', methods=['GET', 'POST'])
def movielist():
	name = str()
	if request.method == 'GET':
		name = request.args.get('title')
	temp = list()
	temp = call_API(name)
	return render_template('movielist.html', items=temp)

if __name__ == "__main__":
  app.run()
