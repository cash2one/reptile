#!/usr/bin/env python
# encoding: utf-8
#   @file: hkmp4.py
#   @Created by shucheng.qu on 2018/10/1

# 好看视频 搞笑类
import json

import requests
from lxml import etree
import datetime
import time
from urllib.parse import unquote
from newreptile.utils.dirs import makedirs
from newreptile.utils.save import save
from newreptile.xigua.xgupload import upload

headers = {'Accept': '*/*',
           'Referer': 'http://sv.baidu.com/',
           'Host': 'sv.baidu.com',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cookie': 'BIDUPSID=DC7BBC3BF80F0B4D394DD93F2BB79D54; PSTM=1481187061; __cfduid=d883c5690f8d164a8ffb5fc98785afea01532575554; MCITY=-%3A; BAIDUID=6EF572039DBDE67795CA0B1D3B168F3D:FG=1; BDUSS=VxdH5wcU5LNFlELUVUY0I5WnRiOTZkSlZLd2tlZGJQeFItaXg2OXhSQmY3TmRiQUFBQUFBJCQAAAAAAAAAAAEAAAAHBBkv0KHR-cTju7nMq8TbAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF9fsFtfX7BbOH; H_PS_PSSID=; BDSFRCVID=iqIsJeC62mKG9Gv746-hUwaJC6UvQ0nTH6aoeJkF9j62l-hHUbCBEG0PjU8g0KubKli5ogKKBmOTHgbP; H_BDCLCKID_SF=fRKJVIIKtIvMj6rmbtOhq4tHeULqJnJZ5mAqoq3daqothI0mqfrG5-Q-Wxb-hp3OHmQnaIQqW4jU8UKl5P45yMIi04AOJxJ43bRTKPPy5KJvfj6g5UQ4hP-UyN0HWh37MJcTVD_atKKMMDDmenJb5ICthfny5K62aKDs0fJo-hcqEIL4eqrtjpDwjN8qbpQPbK6Z5KQ8JqTbHUbSj4QzQCuvKfLeaMni52jQhD5typ5nhMJe3j7JDMP0-l620njy523i5J6vQpnJHxtuD682jTjLDGDsbncJ2IOXsJT2MnbSKROkePrayJtpbt-qJtri3b5xLD02Jj6sSt3pyx--3JKuDMTnBT5KaKTZBhLX2DLKD56dyhoDLUDkQN3TaqLO5bRiLRocanIhDn3oyU5VXp0nbU5TqtJHKbDHoIDbtfK; delPer=0; PSINO=1',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

# tabs = ['doubiju', 'qiongying', 'zhibo', 'yinyuetai', 'news', 'zuiyule', 'aishenghuo', 'xiaopin', 'youxi', 'military','waiguoren', 'edu', 'mengmengda', 'tech', 'tiyu', 'dongman']
tabs = ['doubiju', 'zuiyule']
# 'Goman'
path = makedirs('haokan', 'Goman')
for tab in tabs:
    for index in range(1, 50):
        url = f'http://sv.baidu.com/videoui/list/tab?source=wise-channel&pd=&subTab={tab}&direction=down&refreshType=0&ua=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36&bt=1538392168&caller=bdwise&_={int(round(time.time() * 1000))}&cb=jsonp{index}'
        html = json.loads(
            requests.get(url, headers=headers).content.decode('utf-8').replace(f'jsonp{index}(', '').replace('})',
                                                                                                             '}'))[
            'data']['tpl']
        html = f'<!doctype html><html lang="en"><head></head><body >{html}</body></html>'
        lis = etree.HTML(html).xpath('/html/body/li')
        for li in lis:
            try:
                mpurl = li.xpath('./div/@data-vsrc')[0]
                mptitle = li.xpath('./div/@data-title')[0]
                count = li.xpath('./div/div[1]/div[1]/div[2]/div[1]/p/text()')[0]
                if mptitle == '' or mpurl == '':
                    print('爬到一条广告，跳过去！')
                    continue
                if '万' in count and int(float(count[0:count.index('万')])) > 5:
                    print(mptitle + '   ' + str(count) + '   ' + mpurl)
                    mptitle = mptitle.replace('/', '')
                    time.sleep(1)
                    count = count[0:count.index('万')]
                    name_path = f'{path}/{count}{mptitle}.mp4'
                    save(name_path, mpurl)
                    upload(name_path)
            except Exception as e:
                print(e)
        print(f'好看视频之{tab}    爬虫第 {index} 页完成')
