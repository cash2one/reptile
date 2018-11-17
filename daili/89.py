#!/usr/bin/env python
# encoding: utf-8
#   @file: 89.py
#   @Created by shucheng.qu on 2018/11/15


# http://www.89ip.cn/index_1.html


import requests
import time
from lxml import etree


def getProxy():
    ips = []
    with open('111.txt', 'r') as ipp:
        for line in ipp:
            line = line.replace('\n','')
            ip = line.split(':')
            proxy_ip = F'http://{ip[0]}:{ip[1]}'
            ips.append(proxy_ip)
    return ips


def request():
    ips = getProxy()
    uu = 'http://yh.mj70.cn/?id=917361050'
    print('start')
    for ip in ips:
        try:
            proxies = {"http": ip}
            print(requests.get(uu, proxies=proxies).content)
        except Exception as e:
            print(e)


# proxies= {"http": 'http://112.95.206.74:8888'}
# print(requests.get('http://yh.mj70.cn/?id=917361050',proxies=proxies).content)
for index in range(0, 10):
    # request()
    request()
    break
