#!/usr/bin/env python
# encoding: utf-8
#   @file: pdl.py
#   @Created by shucheng.qu on 2018/11/14


# http://www.xicidaili.com/wt/2
import requests
import time
from lxml import etree


proxy_dict = {
    "http": "http://username:password@hogehoge.proxy.jp:8080/",
    "https": "http://username:password@hogehoge.proxy.jp:8080/"
}

def getProxy():
    ips = []
    for index in range(1, 100):#每页15个
        url = F'https://www.kuaidaili.com/free/intr/{index}/'
        htmls = requests.get(url).content.decode('utf-8')
        trs = etree.HTML(htmls).xpath('//*[@id="list"]/table/tbody/tr')
        for tr in trs:
            ip = tr.xpath('./td[1]/text()')[0]
            port = tr.xpath('./td[2]/text()')[0]
            proxy_ip = F'http://{ip}:{port}'
            ips.append(proxy_ip)
        time.sleep(2)
    return ips

def request():
    ips = getProxy()
    uu = 'http://yh.mj70.cn/?id=917361050'
    for ip in ips:
        try:
            proxies = {"http": ip}
            print(requests.get(uu, proxies=proxies).content)
        except Exception as e:
            print(e)


# proxies= {"http": 'http://112.95.206.74:8888'}
# print(requests.get('http://yh.mj70.cn/?id=917361050',proxies=proxies).content)
request()