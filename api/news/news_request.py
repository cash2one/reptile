#!/usr/bin/env python
# encoding: utf-8
#   @file: news_request.py
#   @Created by shucheng.qu on 2018/10/24
import json

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
        return 'error'


if __name__ == '__main__':
    pass