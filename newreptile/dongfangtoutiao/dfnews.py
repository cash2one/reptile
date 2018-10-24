#!/usr/bin/env python
# encoding: utf-8
#   @file: dfnews.py
#   @Created by shucheng.qu on 2018/10/24
import hashlib
import json

import requests
from lxml import etree
import datetime
import time
from urllib.parse import unquote

from db.mysql import getdb, closedb
from db.newsdb import save_db
from newreptile.utils.dirs import makedirs

from newreptile.utils.save import save

junshi = 'https://toutiao.eastday.com/toutiao_h5/RefreshJP?type=junshi&recgid=15400109447415339&qid=xiaochengxu_dftt&picnewsnum=1&readhistory=181019111609470&zdnews=181024082103159&idx=0&pgnum=1&os=iOS%2012.1'
yule = 'https://toutiao.eastday.com/toutiao_h5/RefreshJP?type=yule&recgid=15400109447415339&qid=xiaochengxu_dftt&picnewsnum=1&readhistory=181019111609470&zdnews=181024085041694&idx=0&pgnum=1&os=iOS%2012.1'
shehui = 'https://toutiao.eastday.com/toutiao_h5/RefreshJP?type=shehui&recgid=15400109447415339&qid=xiaochengxu_dftt&picnewsnum=1&readhistory=181019111609470&zdnews=181024082103159&idx=0&pgnum=1&os=iOS%2012.1'
tiyu = 'https://toutiao.eastday.com/toutiao_h5/RefreshJP?type=tiyu&recgid=15400109447415339&qid=xiaochengxu_dftt&picnewsnum=1&readhistory=181019111609470&zdnews=181024091710716&idx=0&pgnum=1&os=iOS%2012.1'
keji = 'https://toutiao.eastday.com/toutiao_h5/RefreshJP?type=keji&recgid=15400109447415339&qid=xiaochengxu_dftt&picnewsnum=1&readhistory=181019111609470&zdnews=181024084648220&idx=0&pgnum=1&os=iOS%2012.1'
gaoxiao = 'https://toutiao.eastday.com/toutiao_h5/RefreshJP?type=xiaohua&recgid=15400109447415339&qid=xiaochengxu_dftt&picnewsnum=1&readhistory=181019111609470&zdnews=181024092158200&idx=0&pgnum=1&os=iOS%2012.1'
qiche = 'https://toutiao.eastday.com/toutiao_h5/RefreshJP?type=qiche&recgid=15400109447415339&qid=xiaochengxu_dftt&picnewsnum=1&readhistory=181019111609470&zdnews=181024091147625&idx=0&pgnum=1&os=iOS%2012.1'
youxi = 'https://toutiao.eastday.com/toutiao_h5/RefreshJP?type=youxi&recgid=15400109447415339&qid=xiaochengxu_dftt&picnewsnum=1&readhistory=181019111609470&zdnews=181024091543050&idx=0&pgnum=1&os=iOS%2012.1'

# type gaoxiao keji tiyu yule lishi junshi sannong meishi qiwen qiche xinlixue youxi redian
map = {'yule': yule, 'gaoxiao': gaoxiao, 'keji': keji, 'tiyu': tiyu, 'junshi': junshi, 'qiche': qiche, 'youxi': youxi,
       'sannong': shehui}

db = getdb()

for index in range(1, 20000):
    for type, url in map.items():
        content = requests.get(url).content.decode('utf-8')
        lens = len(content)
        content = content[5:lens - 1]
        print(content)
        datas = json.loads(content)['data']
        for data in datas:
            title = data['topic']
            play = data['urlpv']
            miniimg = data['miniimg']
            cover_all = ''
            if len(miniimg) > 0:
                for cc in miniimg:
                    cover_all += cc['src']
                    cover_all += ';'
            news_url = data['url']
            content_decode = requests.get(news_url).content.decode('utf-8')
            divs = etree.HTML(content_decode).xpath('//*[@id="content"]/*')
            txt = []
            for div in divs:
                text = div.xpath('./text()')
                src = div.xpath('./a/img/@src')
                if len(src) > 0:
                    txt.append(src[0])
                    txt.append('\n')
                    continue
                if len(text) > 0:
                    txt.append(text[0])
                    txt.append('\n')
            print(title + play)
            save_db(db, title=title, type=type, cover=cover_all, content=''.join(txt),
                            url=news_url, play=play, author=data['source'],
                            data=time.strftime("%Y/%m/%d %H:%M", time.localtime(data['ctrtime'] / 1000)))
            time.sleep(2)
        print(F'{type} 类型数据完成一页')
    print(F'第 {index} 页完成')
closedb(db)
