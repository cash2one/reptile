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

from db.mysql import getdb, closedb
from db.newsdb import save_db
from newreptile.jinritoutiao.ascp import getASCP
from newreptile.utils.dirs import makedirs
from newreptile.utils.save import save
from selenium import webdriver

headers = {

    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'upgrade-insecure-requests':'1',
    'cache-control':'no-cache',
    'x-requested-with': 'XMLHttpRequest',
    'postman-token':'965b6241-7ec5-9e1a-4e99-9dca987180f1',
    'cookie': 'UM_distinctid=16618b95ff8fec-0fa240b9021b02-346a7809-13c680-16618b95ff962c; ccid=296a02fee1cb2bde36141ce9b5fb805b; csrftoken=e4fffe94a5bcf52adaa6721377f3390c; tt_webid=6605715939382117896; tt_webid=6605715939382117896; WEATHER_CITY=%E5%8C%97%E4%BA%AC; odin_tt=262ede1235a3aeabad5bf1c22afdcce2e084b30e253823fdf3ceff9e01357cc2c7669544ca3074e1a37bc85418daaa04; toutiao_sso_user=c74691eabf1d099ea05c0454cf743e59; sso_login_status=1; login_flag=ba6e0a6676bb4d786cfdb690ba7205ba; sessionid=44d6b943ce601a25e0ce8e16c35bed71; sid_tt=44d6b943ce601a25e0ce8e16c35bed71; sso_uid_tt=d34e114a7e1528a0672cad21666554ce; uid_tt=e811dd21e8eb1b56ce7fd04963da74ea; sid_guard="44d6b943ce601a25e0ce8e16c35bed71|1538033885|15552000|Tue\054 26-Mar-2019 07:38:05 GMT"; uuid="w:de2c0423770643e5a4cc4a740d70f61e"; __tea_sdk__ssid=beec8374-ce22-4c85-85e8-0c0ec8728c41; _ga=GA1.2.690585305.1538033999; __tea_sdk__user_unique_id=104777979000; __utma=24953151.690585305.1538033999.1538793328.1538793328.1; __utmz=24953151.1538793328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); CNZZDATA1259612802=1521346509-1538012542-%7C1540531590; __tasessionId=5a5jn5syg1540534841730; Hm_lvt_407473d433e871de861cf818aa1405a1=1540534850; Hm_lpvt_407473d433e871de861cf818aa1405a1=1540534850',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

# 娱乐新闻
api = 'https://www.toutiao.com'

gaoxiao = 'funny'
qiche = 'news_car'
tiyu = 'news_sports'
youxi = 'news_game'
yule = 'news_entertainment'
keji = 'news_tech'
redian = 'news_hot'
junshi = 'news_military'

map = {'gaoxiao':gaoxiao,'redian':redian,'keji':keji,'tiyu':tiyu,'junshi':junshi,'qiche':qiche,'youxi':youxi,
       'yule':yule}

driver = webdriver.Chrome()
db = getdb()
for index in range(0,20000):
    for type,tag in map.items():
        AS, CP = getASCP()
        url = F'https://m.toutiao.com/list/?tag={tag}&ac=wap&count=20&format=json_raw&as={AS}&cp={CP}&min_behot_time=0&_signature=Yv6UpAAAOS-VYPOwyZmrJ2L-lL&i='
        content = requests.get(url, headers=headers).content.decode('utf-8')
        datas = json.loads(content)['data']
        for data in datas:
            if data['has_video'] :
                continue
            new_url = data['display_url']
            title = data['title']
            intro = data['abstract']
            comment = 0
            if 'comment' in data.keys():
                comment = data['comment_count']
            cover = ''
            if 'image_list' in data.keys():
                image_list = data['image_list']
                for item in image_list:
                    cover += item['url']
                    cover += ';'
            driver.get(new_url)
            time.sleep(3)
            source = driver.page_source
            divs = etree.HTML(source).xpath('/html/body/div/div[2]/div[2]/div[1]/div[2]/div/*')
            txt = []
            for div in divs:
                src = div.xpath('./img/@src')
                text = div.xpath('./text()')
                text2 = div.xpath('./ul/li/text()')
                if len(src) > 0:
                    txt.append(src[0])
                    txt.append('\n')
                    continue
                if len(text) > 0:
                    txt.append(text[0])
                    txt.append('\n')
                if len(text2) > 0:
                    txt.append(text2[0])
                    txt.append('\n')
            print(title +'   '+ new_url)
            join = ''.join(txt)
            if len(join) <100:
                continue
            save_db(db, title=title, intro=intro,type=type, cover=cover, content=join,
                    url=new_url, play=comment, author=data['media_info']['name'],author_img=data['media_info']['avatar_url'],
                    data=time.strftime("%Y/%m/%d %H:%M", time.localtime(data['behot_time'])),
                    source='jinritoutiao')
            time.sleep(2)
        print(F'今日头条 {type} 类型')
    print(F'今日头条 爬虫第 {index} 页')
closedb(db)