#!/usr/bin/env python
# encoding: utf-8
#   @file: app.py
#   @Created by shucheng.qu on 2018/10/24

import json

from flask import Flask, request

from api.error import error1
from api.news.news_request import news, news_detail
from api.video.video_request import video

app = Flask(__name__)


#
@app.route('/')
def index():
    return '富强、民主、文明、和谐、自由、平等、公正、法治、爱国、敬业、诚信、友善'

#
@app.route('/api/news', methods=['POST'])
def news_():
    try:
        if request.method == 'POST':
            q = request.form['q']
            key = request.form['sign']
            return news(q, key)
        else:
            return '富强、民主、文明、和谐、自由、平等、公正、法治、爱国、敬业、诚信、友善'
    except Exception as e:
        print(e)
        return error1


@app.route('/api/news/detail', methods=['POST'])
def news_detail_():
    try:
        if request.method == 'POST':
            q = request.form['q']
            key = request.form['sign']
            return news_detail(q, key)
        else:
            return '富强、民主、文明、和谐、自由、平等、公正、法治、爱国、敬业、诚信、友善'
    except Exception as e:
        print(e)
        return error1


@app.route('/api/video', methods=['POST'])
def video_():
    try:
        if request.method == 'POST':
            q = request.form['q']
            key = request.form['sign']
            return video(q, key)
        else:
            return '富强、民主、文明、和谐、自由、平等、公正、法治、爱国、敬业、诚信、友善'
    except Exception as e:
        print(e)
        return error1


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')
