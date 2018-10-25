#!/usr/bin/env python
# encoding: utf-8
#   @file: xgmp4.py
#   @Created by shucheng.qu on 2018/10/4
# 西瓜视频爬虫
import hashlib
import json

import requests
from lxml import etree
import datetime
import time
from urllib.parse import unquote

from db.mysql import getdb, closedb
from db.videodb import save_db
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

api = 'https://www.ixigua.com'

youxi = 'https://www.ixigua.com/api/pc/feed/?min_behot_time=0&category=subv_xg_game&utm_source=toutiao&widen=1&tadrequire=true&as=A185DB8DD1AD131&cp=5BD19DE1F3311E1&_signature=nie08xAUxgIhUUUVEkPvi54ntO'
shenghuo = 'https://www.ixigua.com/api/pc/feed/?min_behot_time=0&category=subv_xg_life&utm_source=toutiao&widen=1&tadrequire=true&as=A195CBED713D178&cp=5BD1DD9187584E1&_signature=nie08xAUxgIhUUUVEkPvi54ntO'
tiyu = 'https://www.ixigua.com/api/pc/feed/?min_behot_time=0&category=subv_sport&utm_source=toutiao&widen=1&tadrequire=true&as=A195CB2D41BD19E&cp=5BD16DE1C94ECE1&_signature=nie08xAUxgIhUUUVEkPvi54ntO'
qiche = 'https://www.ixigua.com/api/pc/feed/?min_behot_time=0&category=subv_car&utm_source=toutiao&widen=1&tadrequire=true&as=A1358BED417D1B9&cp=5BD18DC1FB294E1&_signature=nie08xAUxgIhUUUVEkPvi54ntO'
keji = 'https://www.ixigua.com/api/pc/feed/?min_behot_time=0&category=subv_video_tech&utm_source=toutiao&widen=1&tadrequire=true&as=A1857BBD31CD1F0&cp=5BD1CD115FB01E1&_signature=nie08xAUxgIhUUUVEkPvi54ntO'
yingshi = 'https://www.ixigua.com/api/pc/feed/?min_behot_time=0&category=subv_xg_movie&utm_source=toutiao&widen=1&tadrequire=true&as=A1150B3DC12D20E&cp=5BD11D32402E1E1&_signature=nie08xAUxgIhUUUVEkPvi54ntO'
wenhua = 'https://www.ixigua.com/api/pc/feed/?min_behot_time=0&category=subv_video_culture&utm_source=toutiao&widen=1&tadrequire=true&as=A145FB6DE1BD277&cp=5BD1BDC207C78E1&_signature=nie08xAUxgIhUUUVEkPvi54ntO'

map = {'qiche': qiche, 'yingshi': yingshi, 'qiqu': wenhua,
       'tiyu': tiyu,
       'youxi': youxi, 'shenghuo': shenghuo, 'keji': keji, }
db = getdb()
driver = webdriver.Chrome()
for index in range(1, 20000):
    for type, url in map.items():
        content = requests.get(url, headers=headers).content.decode('utf-8')
        print(content)
        data = json.loads(content)['data']
        for da in data:
            try:
                count = da['video_play_count']
                title = da['title']
                src = api + da['source_url']
                driver.get(src)
                time.sleep(3)
                mp4_src = driver.find_elements_by_xpath('.//video')[0].get_attribute('src')
                mp4_title = da['title']
                print(f'{count}     {mp4_title}     {mp4_src}')
                # save(f'{path}/{mp4_title}{count}.mp4', mp4_src)
                md5 = hashlib.md5()
                md5.update(requests.get(mp4_src).content)
                md5 = md5.hexdigest()
                save_db(db, md5=md5, title=title, url=mp4_src, cover=da['image_url'], play=count,
                        intro=da['abstract'],
                        author=da['source'], author_img=da['media_avatar_url'], type=type, comment=da['comments_count'],
                        data=time.strftime("%Y/%m/%d %H:%M", time.localtime(int(da['behot_time']))),
                        source='xiguashipin')
                time.sleep(1)
            except Exception as e:
                print(e)
        print(F'{type} 类型获取一页')
    print(f'西瓜视频    爬虫第 {index} 页完成')
closedb(db)
