#!/usr/bin/env python
# encoding: utf-8
#   @file: qttnewsupload.py
#   @Created by shucheng.qu on 2018/11/7


import datetime
import json
import math
import random

import requests
import time
import hashlib
from requests import sessions
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests_toolbelt.multipart.encoder import MultipartEncoder

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

img_headers = {
    'Connection': 'keep-alive',
    'Origin': 'https://mp.qutoutiao.net',
    'X_Requested_With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://mp.qutoutiao.net/static/ueditor/dialogs/image/image.html?r=1002',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

save_headers = {
    'Connection': 'keep-alive',
    'Origin': 'https://mp.qutoutiao.net',
    'X_Requested_With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://mp.qutoutiao.net/publish-content/article',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

upload_url = 'https://editer2.1sapp.com/ueditor/php/controller.php?action=uploadimage&encode=utf-8'

saveNew = 'https://mpapi.qutoutiao.net/content/saveNew'


def _upload_img(src):
    try:
        file = requests.get(src, verify=False).content
        split = str(src).split('/')
        name = split[len(split) - 1]
        lens = len(file)
        multipart_encoder = MultipartEncoder(
            fields={
                'id': 'WU_FILE_0',
                'type': 'image/jpeg',
                'name': 'name',
                'lastModifiedDate': time.strftime("%a %b %d %Y %H:%M:%S GMT+0800 (中国标准时间)", time.localtime()),
                'size': str(lens),
                'upfile': (name, file, 'application/octet-stream')
            },
            boundary='----WebKitFormBoundary' + str(random.randint(1e28, 1e29 - 1))
        )
        img_headers['Content-Type'] = multipart_encoder.content_type
        print(requests.options(upload_url, verify=False).content.decode('utf-8'))
        up_part = requests.post(upload_url, data=multipart_encoder, headers=img_headers,
                                verify=False).content.decode('utf-8')
        jsons = json.loads(up_part)
        print(jsons)
        return jsons
    except Exception as e:
        print(e)
        return None


# https://mpapi.qutoutiao.net/content/saveNew
# id	1024424548
# category	7
# two_level_category	[{"id":"100700","name":"笑话段子"},{"id":"100702","name":"GIF动画"},{"id":"100705","name":"其他"}]
# cover_type	1
# cover	["qupost/images/2018/11/07/1541571610132251045.jpg"]
# title	这是表能开机任务接我
# detail	<p>q&#39;w&#39;j&#39;ne几块钱热裤人均可全额，人日记内容经开区</p><p><img data-src="http://static.1sapp.com/image/p/2018/11/07/1541571582423508water.png" data-size="1125,450" style="" title="1541571582423508.png"/></p><p>连接器恩借款人那就快去吧认可今年金额可能人家new</p><p><img data-src="http://static.1sapp.com/image/p/2018/11/07/1541571596565203water.jpg" data-size="1006,1006" style="" title="1541571596565203.jpg"/></p>
# image_list	["image/p/2018/11/07/1541571582423508water.png","image/p/2018/11/07/1541571596565203water.jpg"]
# is_delay	0
# is_origin	1
# tag	我去额,wqljnr,几千万人
# code	44768
# flag_id	article14528521541571560671
# token	8ba8L9bnuaxpR2a9z_CJElZSFHeq3PMqr1OE9MZnpd2PgJgkeHB44q0kmaSc2XuHeYAH3qACaZrQ3_0
# dtu	200


# https://mpapi.qutoutiao.net/content/setLocalChannel
# content_id	1024424548
# local_channel_list	[]
# token	8ba8L9bnuaxpR2a9z_CJElZSFHeq3PMqr1OE9MZnpd2PgJgkeHB44q0kmaSc2XuHeYAH3qACaZrQ3_0
# dtu	200


# https://mpapi.qutoutiao.net/content/changeStatus?id=1024424548&status=5&flag_id=article14528521541571560671&token=8ba8L9bnuaxpR2a9z_CJElZSFHeq3PMqr1OE9MZnpd2PgJgkeHB44q0kmaSc2XuHeYAH3qACaZrQ3_0&dtu=200
# id	1024424548
# status	5
# flag_id	article14528521541571560671
# token	8ba8L9bnuaxpR2a9z_CJElZSFHeq3PMqr1OE9MZnpd2PgJgkeHB44q0kmaSc2XuHeYAH3qACaZrQ3_0
# dtu	200
#
# id
# category	5
# two_level_category	[{"id":"100500","name":"奇闻轶事"},{"id":"100502","name":"未解之谜"},{"id":"100504","name":"猎奇"}]
# cover_type	1
# cover	["qupost/images/2018/11/21/1542767025511382660.jpg"]
# title	金额卫宁健康部分王老吉
# detail	<p>而且将男人接吻<img data-src="http://static.1sapp.com/image/p/2018/11/21/1542766973829429water.jpg" data-size="386,384" title="1542766973829429.jpg" alt="-55f9d2b63d74fb6e.jpg"/></p><p>恳请加入了接吻日进了那我就让你为了你额接吻女人今年文件，内容额外金融界new就让你</p><p><img data-src="http://static.1sapp.com/image/p/2018/11/21/1542767023424909water.png" data-size="198,152" title="1542767023424909.png" alt="25e542acd87208c8.png"/></p>
# image_list	["image/p/2018/11/21/1542766973829429water.jpg","image/p/2018/11/21/1542767023424909.png"]
# is_delay	0
# is_origin	1
# tag	请问焦恩俊,我去bjkq,qwjkeb
# code	7634
# flag_id	article14528521541577217841
# token	be80iB_3qSQ55mRperXY-dz4o4x4sP-wjd2M5nVUTkx6tz8Kp2MeHyWr68NzSaTzI3IwswJpw_UfJJw
# dtu	200

def upload_news(title, txt):
    content = []
    for sp in txt:
        if sp.startswith('http'):
            jsons = _upload_img(sp)
            if jsons == None:
                continue
            img = F'<div class="pgc-img"><img class="" src="{jsons["url"]}" data-ic="false" data-ic-uri="" data-height="{jsons["height"]}" data-width="{jsons["width"]}" image_type="{jsons["image_type"]}" web_uri="{jsons["wm_uri_media"]}" img_width="{jsons["width"]}" img_height="{jsons["height"]}"><p class="pgc-img-caption"></p></div>'
            img = F'<p><img data-src="http://static.1sapp.com/image{jsons["url"]}" data-size="198,152" title="{jsons["title"]}" alt="25e542acd87208c8.png"/></p>'
            content.append(img)
            continue
        content.append(F'<p>{sp}</p>')
    # requests.get('https://mp.toutiao.com/media/permissions/article/post/',headers=o_headers,verify=False).content.decode('utf-8')
    param = {
        'id': '',
        'category': '5',
        'two_level_category': '[{"id":"100500","name":"奇闻轶事"},{"id":"100502","name":"未解之谜"},{"id":"100504","name":"猎奇"}]',
        'cover_type': '1',
        'cover': '["qupost/images/2018/11/21/1542767025511382660.jpg"]',
        'title': f'{title}',
        'detail': ''.join(content),
        'image_list': [],
        'is_delay': '0',
        'is_origin': '1',
        'tag': '',
        'code': '7634',
        'flag_id': 'article14528521541577217841',
        'token': 'be80iB_3qSQ55mRperXY-dz4o4x4sP-wjd2M5nVUTkx6tz8Kp2MeHyWr68NzSaTzI3IwswJpw_UfJJw',
        'dtu': '200'}
    result = requests.post(saveNew, data=param, headers=save_headers, verify=False).content.decode('utf-8')
    print(result)


if __name__ == "__main__":
    # upload_news('/Users/macbook-HCI/pachong/news/1012/qtt/1111.txt')
    print()

    _upload_img('https://img.haoyangmao8.com/zb_users/upload/2018/03/201803187623_11.jpeg')

    pass
