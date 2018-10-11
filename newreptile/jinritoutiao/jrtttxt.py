#!/usr/bin/env python
# encoding: utf-8
#   @file: jrtttxt.py
#   @Created by shucheng.qu on 2018/10/9
# 今日头条图文新闻爬虫
import json

import requests
from lxml import etree
import datetime
import time
from urllib.parse import unquote
from newreptile.utils.dirs import makedirs
from newreptile.utils.save import save
from selenium import webdriver

headers = {
    # ':authority': 'www.ixigua.com',
    # ':method': 'GET',
    # ':scheme': 'https',
    'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'referer': 'https://www.ixigua.com/',
    'x-requested-with': 'XMLHttpRequest',
    'Cookie': '_ga=GA1.2.2015676264.1538264960; tt_webid=6607536731519206920; WEATHER_CITY=%E5%8C%97%E4%BA%AC; _gid=GA1.2.1949152419.1538633534; UM_distinctid=1663db48be2674-01da60aa84ec03-346a7809-13c680-1663db48be3744; CNZZDATA1262382642=134620746-1538629770-https%253A%252F%252Fwww.baidu.com%252F%7C1538629770; __tasessionId=dwywyvbwu1538633534853',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

ttheaders = {'SIID': '612697538645; _gat=1', 'Host': 'service0.iiilab.com', 'Origin': 'http://toutiao.iiilab.com',
             'Referer': 'http://toutiao.iiilab.com/'}
# 娱乐新闻
url = 'https://www.toutiao.com/api/pc/feed/?category=news_entertainment&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1151B6BBC13C8F&cp=5BBC33DCC8BF2E1&_signature=x2jGTQAAnN54HjerAssjDMdoxl'
api = 'https://www.toutiao.com'
path = makedirs('jinritt', 'yule')
driver = webdriver.Chrome('/Users/macbook-HCI/Downloads/pachong/chromedriver')
for index in range(0,100):
    content = requests.get(url, headers=headers).content.decode('utf-8')
    datas = json.loads(content)['data']
    for data in datas:
        new_url = api+data['source_url']
        driver.get(new_url)
        time.sleep(3)
        try:
            divs = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div')
            print(divs)
            break
        except Exception as e:
            print(e)


