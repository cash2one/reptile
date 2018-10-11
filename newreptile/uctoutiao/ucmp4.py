#!/usr/bin/env python
# encoding: utf-8
#   @file: ucmp4.py
#   @Created by shucheng.qu on 2018/10/6
# UC头条视频  奇趣
import json

import requests
from lxml import etree
import datetime
import time
from urllib.parse import unquote
from newreptile.utils.dirs import makedirs
from newreptile.utils.save import save
from selenium import webdriver

from newreptile.xigua.xgupload import upload

url = 'http://iflow.uczzd.cn/iflow/api/v1/channel/622777922?app=ucnews-iflow&recoid=8616764939547547119&ftime=1538793113055&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1538793737078&sign=Kvi0z7u7iZHh6W%2BGzro%2BkJ1fyNsasa%2FLpxPonGPeFLbRrXkAWoIxB9fxbgG3nFeEGiA%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvlrWWXvPPLnq%2bEh3ch9b4GfGFlFTuPKP6DwglnnjHDX7A%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'

path = makedirs('uc', 'Goman')

driver = webdriver.Chrome()

for index in range(1, 200):
    data = json.loads(requests.get(url).content.decode('utf-8'))['data']
    items = data['items']
    for item in items:
        article = data[item['map']][item['id']]
        zzd_url = article['zzd_url']
        title = article['title']
        view_cnt = article['view_cnt']
        if view_cnt > 40000:
            view_cnt = int(view_cnt / 10000)
            driver.get(zzd_url)
            time.sleep(3)
            try:
                mp4_src = driver.find_elements_by_xpath('.//video')[0].get_attribute('src')
                print(f'{title}   {view_cnt}万    {mp4_src}')
                name_path = f'{path}/{view_cnt}{title}.mp4'
                save(name_path, mp4_src)
                upload(name_path)
            except Exception as e:
                print(e)
    print(f'UC视频 奇趣    爬虫第 {index} 页完成')
