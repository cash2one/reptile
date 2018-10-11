#!/usr/bin/env python
# encoding: utf-8
#   @file: xgmp4.py
#   @Created by shucheng.qu on 2018/10/4
# 西瓜视频爬虫
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

url = 'https://www.ixigua.com/api/pc/feed/?min_behot_time=0&category=video_new&utm_source=toutiao&widen=1&tadrequire=true&as=A1A51BEB750B876&cp=5BB5BB28D7469E1&_signature=b51JGhAXNCzQ67j8HOfuSW-dSQ'
api = 'https://www.ixigua.com'

path = makedirs('xigua', 'Goman')

driver = webdriver.Chrome()

for index in range(1, 200):
    content = requests.get(url, headers=headers).content.decode('utf-8')
    data = json.loads(content)['data']
    for da in data:
        try:
            count = da['video_play_count']
            if count > 50000:
                count = int(count / 10000)
                src = api + da['source_url']
                driver.get(src)
                time.sleep(3)
                mp4_src = driver.find_elements_by_xpath('.//video')[0].get_attribute('src')
                mp4_title = da['title']
                print(f'{count}     {mp4_title}     {mp4_src}')
                save(f'{path}/{mp4_title}{count}.mp4', mp4_src)
        except Exception as e:
            print(e)
    print(f'西瓜视频    爬虫第 {index} 页完成')
