#!/usr/bin/env python
# encoding: utf-8
#   @file: news_request.py
#   @Created by shucheng.qu on 2018/10/24
import json

from api.error import error1
from api.news.detail.detail1 import detail1_result
from api.news.news1.new1 import news1_result


def news(q,key):
    try:
        data = json.loads(q)
        version = data['version']
        if version ==1:
            return news1_result(q)
        elif version ==2:
            pass
        else:
            pass
    except Exception:

        return error1

def news_detail(q,key):
    try:
        data = json.loads(q)
        version = data['version']
        if version ==1:
            return detail1_result(q)
        elif version ==2:
            pass
        else:
            pass
    except Exception:
        return error1


if __name__ == '__main__':
    pass