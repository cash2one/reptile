#!/usr/bin/env python
# encoding: utf-8
#   @file: test.py
#   @Created by shucheng.qu on 2018/10/9
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests_toolbelt.multipart.encoder import MultipartEncoder

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# User-Agent	Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N9100 Build/MMB29M) hsp
# Content-Type	application/encrypted-json
# Accept	application/encrypted-json
# Host	api.cashtoutiao.com
# Accept-Encoding	gzip
# Content-Length	304
# Connection	keep-alive

header = {'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N9100 Build/MMB29M) hsp',
          'Content-Type':'application/encrypted-json',
          'Accept':'application/encrypted-json',
          'Accept-Encoding':'gzip',
          'Connection':'keep-alive'}


# text = '''?Ôj:Yy.q@L[õÀQ,Bdg	ûç]§dÉ.Îx6ÎÃÛÌÿ\#]{Û°´Ø£¡IFf¾<ÉîÚ{d-é?
# 4h2Ñ¤ObZv|ú9bW¿£ù~]»FaÃéhªéæcÌ/Ê)Mín¶(ªº0¸X)±®É RÞsrø;XP2b`0Bn+MhÞ;t@z5JÕî	fÛyXâ6}øIÑ~]ýº¾Ðlñµ{ßÔ{>^^Éa¹¥ÓEÿ*iDÈqÊº¢ãíûü]Xlå¹w«$ùø»ãw©Áýz¹ð£	õ'Å5E3 ×A¨¸3Ü5"ÜÉ­öÖö'''

# text = 'fewfewfewfew'

# url = 'http://api.cashtoutiao.com/frontend/read/sych/duration?userId=125411722&loginId=eab4529fda694329a60d20590941d20d'
# param = {'userId':'125411722','loginId':'eab4529fda694329a60d20590941d20d'}

# requests.post(url,data=text,verify=False)


# 	GET /activity/digTreasure/conf HTTP/1.1
# base-key	3R11BreSbEWXPKMxJQSwiPkgtkC7PjlzH4rmfQV4yPsco5ohrBjdo2zmXHm2f__B5jzJb-k4-PycctocJI1HKw==
# Host	xwz.coohua.com
# Connection	Keep-Alive
# Accept-Encoding	gzip
# User-Agent	okhttp/3.10.0



hh = {'base-key':'3R11BreSbEWXPKMxJQSwiPkgtkC7PjlzH4rmfQV4yPsco5ohrBjdo2zmXHm2f__B5jzJb-k4-PycctocJI1HKw==','User-Agent':'okhttp/3.10.0',
      'Accept-Encoding':'gzip','Connection':'Keep-Alive'}


ffhh = {'base-key':'3R11BreSbEWXPKMxJQSwiPkgtkC7PjlzH4rmfQV4yPsco5ohrBjdo2zmXHm2f__B5jzJb-k4-PycctocJI1HKw==',
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'okhttp/3.10.0',
      'Accept-Encoding':'gzip','Connection':'Keep-Alive'}

lll = 'https://xwz.coohua.com/activity/digTreasure/conf'
fff = 'https://xwz.coohua.com/reward/refresh'

params = 'rnd=26&sign=AF913731EBA6C9CABC1DB611551F12E2&newsId=9966282_1&type=read&os=android&isRefresh=0'
print(requests.post(fff,headers=ffhh,data = params,verify=False).content.decode('utf-8'))

print(requests.get(lll,headers=hh,verify=False).content.decode('utf-8'))


time.sleep(0.8)

print(requests.post('https://xwz.coohua.com/task/bubble',headers=ffhh,verify=False).content.decode('utf-8'))