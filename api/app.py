#!/usr/bin/env python
# encoding: utf-8
#   @file: app.py
#   @Created by shucheng.qu on 2018/10/24

import json

from flask import Flask, request

from api.news.news_request import news

app = Flask(__name__)
#
@app.route('/api/news',methods=['POST'])
def news_():
    try:
        if request.method == 'POST':
            q = request.form['q']
            key = request.form['sign']
            return news(q,key)
    except Exception as e:
        print(e)
        return 'error'


if __name__ == '__main__':
    app.run()