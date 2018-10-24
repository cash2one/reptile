#!/usr/bin/env python
# encoding: utf-8
#   @file: dfvideo.py
#   @Created by shucheng.qu on 2018/10/24

import hashlib
import json

import requests
from lxml import etree
import datetime
import time
from urllib.parse import unquote

from selenium import webdriver

from db.mysql import getdb, closedb
from db.videodb import save_db

gaoxiao = 'https://vdh5socket.dftoutiao.com/videoh5/getvideos?type=vgaoxiao&startkey=7683026544338518080%7C700001%7C%7C%7C&lastkey=&pgnum=-2&idx=-11&readhistory=181019142702912116385%2C181019142702912116385%2C180930194601917394927%2C181019175934086224152%2C180929131944174211040&recgid=15400109447415339&qid=xiaochengxu_dftt&os=iOS%2012.1'
yule = 'https://vdh5socket.dftoutiao.com/videoh5/getvideos?type=vyule&startkey=&recgid=15400109447415339&qid=xiaochengxu_dftt&domain=eastday.com&readhistory=181019142702912116385%2C181019142702912116385%2C180930194601917394927%2C181019175934086224152%2C180929131944174211040&idx=1&pgnum=1&os=iOS%2012.1'
youxi = 'https://vdh5socket.dftoutiao.com/videoh5/getvideos?type=vyouxi&startkey=&recgid=15400109447415339&qid=xiaochengxu_dftt&domain=eastday.com&readhistory=181019142702912116385%2C181019142702912116385%2C180930194601917394927%2C181019175934086224152%2C180929131944174211040&idx=1&pgnum=1&os=iOS%2012.1'
shehui = 'https://vdh5socket.dftoutiao.com/videoh5/getvideos?type=vpaike&startkey=&recgid=15400109447415339&qid=xiaochengxu_dftt&domain=eastday.com&readhistory=181019142702912116385%2C181019142702912116385%2C180930194601917394927%2C181019175934086224152%2C180929131944174211040&idx=1&pgnum=1&os=iOS%2012.1'
keji = 'https://vdh5socket.dftoutiao.com/videoh5/getvideos?type=vkeji&startkey=&recgid=15400109447415339&qid=xiaochengxu_dftt&domain=eastday.com&readhistory=181019142702912116385%2C181019142702912116385%2C180930194601917394927%2C181019175934086224152%2C180929131944174211040&idx=1&pgnum=1&os=iOS%2012.1'
qiche = 'https://vdh5socket.dftoutiao.com/videoh5/getvideos?type=vqiche&startkey=&recgid=15400109447415339&qid=xiaochengxu_dftt&domain=eastday.com&readhistory=181019142702912116385%2C181019142702912116385%2C180930194601917394927%2C181019175934086224152%2C180929131944174211040&idx=1&pgnum=1&os=iOS%2012.1'
tiyu = 'https://vdh5socket.dftoutiao.com/videoh5/getvideos?type=vtiyu&startkey=&recgid=15400109447415339&qid=xiaochengxu_dftt&domain=eastday.com&readhistory=181019142702912116385%2C181019142702912116385%2C180930194601917394927%2C181019175934086224152%2C180929131944174211040&idx=1&pgnum=1&os=iOS%2012.1'
shenghuo = 'https://vdh5socket.dftoutiao.com/videoh5/getvideos?type=vshenghuo&startkey=&recgid=15400109447415339&qid=xiaochengxu_dftt&domain=eastday.com&readhistory=181019142702912116385%2C181019142702912116385%2C180930194601917394927%2C181019175934086224152%2C180929131944174211040&idx=1&pgnum=1&os=iOS%2012.1'


map = {'gaoxiao': gaoxiao, 'qiche': qiche, 'yule': yule, 'shehui': shehui,
           'tiyu': tiyu,
           'youxi': youxi, 'shenghuo': shenghuo, 'keji': keji, }

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
            print(title)
            play = data['urlpv']
            miniimg = data['miniimg']
            mp4_src = data['video_link']
            md5 = hashlib.md5()
            md5.update(requests.get(mp4_src).content)
            md5 = md5.hexdigest()
            save_db(db, md5=md5, title=title, url=mp4_src, cover=data['miniimg'][0]['src'], play=play,
                    author=data['source'], type=type,
                    data=data['date'])
            time.sleep(3)
        print(F'{type} 类型数据完成一页')
    print(F'第 {index} 页完成')
closedb(db)