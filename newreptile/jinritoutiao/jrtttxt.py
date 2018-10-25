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
from requests.packages.urllib3.exceptions import InsecureRequestWarning

headers = {

    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'upgrade-insecure-requests':'1',
    'cache-control':'no-cache',
    'x-requested-with': 'XMLHttpRequest',
    'cookie': 'tt_webid=6616310778113328654',
    'postman-token':'a61919c3-4039-8fb2-a2de-560c2fd4b518',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

# :method	GET
# :authority	www.toutiao.com
# :scheme	https
# :path	/api/pc/feed/?category=funny&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A155DB5D017D7D2&cp=5BD13DF79DE20E1&_signature=YrnvZAAAOWvdzx6C7NgUk2K573
# accept-language	zh-CN,zh;q=0.9
# upgrade-insecure-requests	1
# user-agent	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36
# content-type	application/x-www-form-urlencoded
# accept	text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# cache-control	no-cache
# x-requested-with	XMLHttpRequest
# postman-token	80421a31-6510-987b-af10-9ab6036c78fc
# accept-encoding	gzip, deflate, br
# cookie	tt_webid=6616310778113328654


ttheaders = {'SIID': '612697538645; _gat=1', 'Host': 'service0.iiilab.com', 'Origin': 'http://toutiao.iiilab.com',
             'Referer': 'http://toutiao.iiilab.com/'}
# 娱乐新闻
api = 'https://www.toutiao.com'

gaoxiao = 'https://www.toutiao.com/api/pc/feed/?category=funny&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A155DB5D017D7D2&cp=5BD13DF79DE20E1&_signature=YrnvZAAAOWvdzx6C7NgUk2K573'
qiche = 'https://www.toutiao.com/api/pc/feed/?category=news_car&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1A5AB8DD1ED80D&cp=5BD18DC8F09D4E1&_signature=YnLbVQAAOabdBCqzQVOy7mJy20'
tiyu = 'https://www.toutiao.com/api/pc/feed/?category=news_sports&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A195DB9DB19D834&cp=5BD1AD8833047E1&_signature=YhuJWQAAOc3dbXi.7k-aJmIbiU'
youxi = 'https://www.toutiao.com/api/pc/feed/?category=news_game&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1256BCD310D846&cp=5BD10D789406BE1&_signature=Yg2Q9wAAOd.de2ERJ6HKiGINkO'
yule = 'https://www.toutiao.com/api/pc/feed/?category=news_entertainment&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A175BB5DD1CD857&cp=5BD1AD188527DE1&_signature=YjyosAAAOfDdSllW7QJIp2I8qK'
keji = 'https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1F57BCDA10D86F&cp=5BD15DC806BFEE1&_signature=YdS6XwAAOgjeoku5NXOQ42HUuk'
redian = 'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A155CB7D317D87F&cp=5BD1CDF8F7AF5E1&_signature=YcTsyAAAOhjesh0uLWjac2HE7N'
junshi = 'https://www.toutiao.com/api/pc/feed/?category=news_military&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1953B9DD16D898&cp=5BD1EDD839C8BE1&_signature=Yf-smQAAOjHeiV1.sLj5M2H.rI'

map = {'gaoxiao':gaoxiao,'redian':redian,'keji':keji,'tiyu':tiyu,'junshi':junshi,'qiche':qiche,'youxi':youxi,
       'yule':yule}

driver = webdriver.Chrome()
for index in range(0,20000):
    for type,url in map.items():
        print( type)
        print(url)
        content = requests.get(url, headers=headers, verify=False).content.decode('utf-8')
        print(content)
        datas = json.loads(content)['data']
        for data in datas:
            new_url = api+data['source_url']
            print(new_url)
            driver.get(new_url)
            time.sleep(3)
            source = driver.page_source
            divs = etree.HTML(source).xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/*')
            txt = []
            for div in divs:
                img = div.xpath('./@src')
                text = div.xpath('./text()')

                print(img)
                print(text)
            break
        break
    break
