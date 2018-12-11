#!/usr/bin/env python
# encoding: utf-8
#   @file: ucmp4.py
#   @Created by shucheng.qu on 2018/10/6
# UC头条视频  奇趣
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

from newreptile.xigua.xgupload import upload
from newreptile.xigua.xgupload import uploadBr

url = 'http://iflow.uczzd.cn/iflow/api/v1/channel/622777922?app=ucnews-iflow&recoid=8616764939547547119&ftime=1538793113055&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1538793737078&sign=Kvi0z7u7iZHh6W%2BGzro%2BkJ1fyNsasa%2FLpxPonGPeFLbRrXkAWoIxB9fxbgG3nFeEGiA%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvlrWWXvPPLnq%2bEh3ch9b4GfGFlFTuPKP6DwglnnjHDX7A%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'

url = F'http://iflow.uczzd.cn/iflow/api/v1/channel/10259?app=ucnews-iflow&recoid=14249534523227927903&ftime={int(round(time.time() * 1000))}&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539410529132&sign=KvjOi729wA8ICN8OVyVivaYeoJJtTLpWyVo82kTo6o6oP6ZId0bDW6Eki1uAX9%2ByI6Q%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmPRyJq%2fAHkMTtoi7ZLTRCR6igsNZAPKky80qy7E8hgGD%2bX4zQjxHsDtDCk%2f%2fxAB%2fUnkgPlSeeN6UgI3ALV%2b%2fQz&gp=KvmMR2ck7BQOrdCGZS3Mm2RS9YXWk0i2tI4Jyzz7dEI4oQ%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'

# 音乐
music = 'http://iflow.uczzd.cn/iflow/api/v1/channel/622336449?app=ucnews-iflow&recoid=4436707331691344676&ftime=1539482498094&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539482622949&sign=Kvia4sM9LAOXgh7wXg3cWAOORqerk8VxiBpOYfgaJRTriXVtJK13DQDAfSKDw9d%2BVMg%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 影视
video = 'http://iflow.uczzd.cn/iflow/api/v1/channel/622769673?app=ucnews-iflow&recoid=9714274250056593310&ftime=1539482502439&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539482700690&sign=Kvi4yLI07o74umOdIDe0KiRP%2FEZh3UJIdxPQXbE4uOouo6g1NYNmF%2FKuBYc73lB4uRs%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 游戏
game = 'http://iflow.uczzd.cn/iflow/api/v1/channel/10051?app=ucnews-iflow&recoid=&ftime=&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539482812758&sign=KvjNW4X0qjkb3nm48KG3hkm7UtN3yQKbjv9%2FbnOBY7n8bSrLFQwqv7OtGnX5xm4uq1E%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 生活
life = 'http://iflow.uczzd.cn/iflow/api/v1/channel/10259?app=ucnews-iflow&recoid=17135928917662427974&ftime=1539410529317&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539482880655&sign=KvhJx4TIohRWKuKneflPzcOUc1W4sNytSlGEE82ydTEIzaKjIiPx0RsOIkaT9QF1CtQ%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 小品
xiaopin = 'http://iflow.uczzd.cn/iflow/api/v1/channel/622810092?app=ucnews-iflow&recoid=1719477496445762902&ftime=1539411755531&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539482912561&sign=KvgGXvDvVeEmzWxh6%2Fh7PgB0hdX0v2IHcLd6PAVWkr3FPfWMoL1ti0SI%2Fbn%2Fwmo96mo%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 综艺
zongyi = 'http://iflow.uczzd.cn/iflow/api/v1/channel/10198?app=ucnews-iflow&recoid=10268692396126839547&ftime=1539411756750&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539482960234&sign=KvhG15MGEyG%2Bcemu%2FeqNLnPTS3a8kQR%2BlAos8ip2z4T1u92X5eBrzSIiUyYnKN4wBps%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 萌物
mengwu = 'http://iflow.uczzd.cn/iflow/api/v1/channel/622485153?app=ucnews-iflow&recoid=9889764153493293010&ftime=1538793700672&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539482996643&sign=Kvhw7CRaMnHxyNVgIKVwyy7nLKc8zMAcZfbIDxYIujeZp%2Fhi%2FCA%2F22%2BC0UplImy8pQA%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 开眼
kaiyan = 'http://iflow.uczzd.cn/iflow/api/v1/channel/622777922?app=ucnews-iflow&recoid=17729968027590137347&ftime=1541860334066&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1541860354595&sign=Kvh8x2lNPG3FJ31tjGaqgcIs28hu%2BGTolGVy7ynXwlwIXDskmMgSj2nCyWruHmlg73A%3D&sc=&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.4.394&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmbnjTrkDHXbdAndlJX9F5r%2bsNehXRMrj206SuPgwKZiA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 体育
tiyu = 'http://iflow.uczzd.cn/iflow/api/v1/channel/10050?app=ucnews-iflow&recoid=&ftime=&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539483078368&sign=Kvjjl8rYc7aTYQfeGF69KcYdUlkaiQthzuOHe0xPG%2FvgUm%2Fms6%2FTsy4gXr6H8kqftoM%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 汽车
qiche = 'http://iflow.uczzd.cn/iflow/api/v1/channel/10038?app=ucnews-iflow&recoid=&ftime=&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539483106570&sign=KviljEk3DJxrYHYScZfsj4gF%2B7wZI%2BcG22JUaOLnR%2FkHLlNv7CpG0p4lj8vL729QZzE%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 演讲
yanjiang = 'http://iflow.uczzd.cn/iflow/api/v1/channel/10295?app=ucnews-iflow&recoid=&ftime=&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539483135360&sign=KvhhSimPofeGaMdOBx0sxCmBwYc9nkQZQUrvPqbYCGUPdROTtSO1m3RzyJWLGUilAQ8%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 创意
chaungyi = 'http://iflow.uczzd.cn/iflow/api/v1/channel/10260?app=ucnews-iflow&recoid=15091573888254580885&ftime=1538791867299&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539483164312&sign=KvhEF5Foq8GADLvcDRvgUdmwDG%2FD5wA9O%2BjS9%2FKOvGdYVJYvFy882%2Bk0Bt0Y%2Bk3B39M%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 热舞
rewu = 'http://iflow.uczzd.cn/iflow/api/v1/channel/10079?app=ucnews-iflow&recoid=1868314393774369899&ftime=1538791811163&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539483190548&sign=Kvjaga2ubmSDWNPZMwIMI9r24K791wYC6dd180waRJ1SprKebYW7Dmra7Z8njLAdEhM%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 现场
xianchang = 'http://iflow.uczzd.cn/iflow/api/v1/channel/622621940?app=ucnews-iflow&recoid=6435793442037426076&ftime=1538791808634&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539483225100&sign=Kvg4Xid5UivYAdjQcaGdtjRS29PKpG4ZFeuOLeR8k%2F1mzPQhj9NWbo13ARBSnya5MCI%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 明星
mingxing = 'http://iflow.uczzd.cn/iflow/api/v1/channel/622726317?app=ucnews-iflow&recoid=1844695229929606644&ftime=1538791803468&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539483255165&sign=KvjoIhP%2F7ZjG1%2BA%2FBlkyH4igA5kTS8Qz0EtoMDZWjvuhu1GEb%2FXHnsX0gq5s2btAHgQ%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# 科技
keji = 'http://iflow.uczzd.cn/iflow/api/v1/channel/10030?app=ucnews-iflow&recoid=12532911498249819381&ftime=1538791799754&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1539483273797&sign=Kvjenmhzjy0n%2BZHgBdCTcUnSqd2ReftnUCZxt%2FPBNsK%2BCb4R%2BQjPIpwSE3ompIsEPw0%3D&sc=&puser=1&tab=video&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvmCqv%2fPJN8tcyDic%2bCU4WMjdEY2LbFQyk1U%2bGxpcj1sYA%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'

map = {'yingshi': video, 'qiche': qiche, 'yinyue': music, 'mengwu': mengwu,
       'tiyu': tiyu,
       'youxi': game, 'yule': mingxing, 'shenghuo': life, 'keji': keji, }

# toutiao = {'video_film': video, 'video_vehicles': qiche, 'video_music': music, 'video_animals': mengwu,
#            'video_sports': tiyu,
#            'video_gaming': game, 'video_entertainment': mingxing, 'video_life': life, 'video_tech': keji, }
# 'video_entertainment': mingxing,
toutiao = {'video_funny': kaiyan }

# path = makedirs('uc', 'Goman')

driver = webdriver.Chrome()
# db = getdb()
for index in range(1, 2000000):
    for k, v in toutiao.items():
        data = json.loads(requests.get(v).content.decode('utf-8'))['data']
        items = data['items']
        for item in items:
            article = data[item['map']][item['id']]
            zzd_url = article['zzd_url']
            title = article['title']
            view_cnt = article['view_cnt']
            print(f'{title}   {view_cnt}')
            # if view_cnt > 50000:
            # view_cnt = int(view_cnt / 10000)
            driver.get(zzd_url)
            time.sleep(3)
            try:
                mp4_src = driver.find_elements_by_xpath('.//video')[0].get_attribute('src')
                print(f'{title}   {view_cnt}    {mp4_src}')
                # name_path = f'{path}/{view_cnt}{title}.mp4'
                # save(name_path, mp4_src)
                # upload(name_path)
                uploadBr(k, F'{title}.mp4', requests.get(mp4_src).content)
                # md5 = hashlib.md5()
                # md5.update(requests.get(mp4_src).content)
                # md5 = md5.hexdigest()
                # save_db(db, md5=md5, title=title, url=mp4_src, cover=article['thumbnails'][0]['url'], play=view_cnt,
                #         comment_url=article['cmt_url'], author=article['site_logo']['desc'],type=k,
                #         author_img=article['site_logo']['img']['url'],
                #         data=time.strftime("%Y/%m/%d %H:%M", time.localtime(int(article['grab_time']/1000))),
                #         source='uctoutiao')
                time.sleep(5)
            except Exception as e:
                print(e)
        print(f'UC视频    爬虫 {k} 类型完成')
    print(f'UC视频    爬虫第 {index} 页完成')
    if index % 5 == 0:
        time.sleep(0.5 * 60 * 60)
driver.close()
# closedb(db)
