#!/usr/bin/env python
# encoding: utf-8
#   @file: save.py
#   @Created by shucheng.qu on 2018/10/5

import requests


def save(path, url):
    with open(path, 'wb') as mp4:
        mp4.write(requests.get(url).content)


def savenews(path, content):
    with open(path, 'w') as txt:
        txt.write(content)
