#!/usr/bin/python
# -*- coding: utf-8 -*-
import trafilatura
import re
import sys
from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)
# 배열 넘겨줄때 방법을 찾아야함.
@app.route('/')
def home():
	if request.method == 'GET':
		return render_template('home.html')

@app.route('/tfidf', methods=['GET', 'POST'])
def tf_idf():
	a = ''
	a = {1:'park', 2:'jung', 3:'kang'}
	return render_template('tfidf.html', result=a)

@app.route('/cosine', methods=['GET', 'POST'])
def cosine():
	cos = ''
	cos = {1:'park', 2:'jung', 3:'kang'}
	return render_template('cosine.html', result=cos)

if __name__ == "__main__":
  app.run()
