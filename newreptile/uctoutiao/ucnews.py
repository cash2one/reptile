#!/usr/bin/env python
# encoding: utf-8
#   @file: ucnews.py
#   @Created by shucheng.qu on 2018/10/23
import hashlib
import json

import requests
from lxml import etree
import datetime
import time
from urllib.parse import unquote

from db.mysql import getdb, closedb
from newreptile.utils.dirs import makedirs
from newreptile.utils.save import save
from selenium import webdriver

gaoxiao = 'http://iflow.uczzd.cn/iflow/api/v1/channel/10013?app=ucnews-iflow&recoid=7411174335971698270&ftime=1539581074761&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1540307389820&sign=KviHAT9duPRcptVek2QaGtUDbI7OJeBWzih46xfyynV7X7pb3%2BTevb9Bai80UjdPOyo%3D&sc=&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvnTtfl94gr0TscDiupliJZ%2baBoA1e70lfYHS4PTJd%2f9FQ%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
keji = 'http://iflow.uczzd.cn/iflow/api/v1/channel/1525483516?app=ucnews-iflow&recoid=4113138831780333906&ftime=1540343809707&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1540343815198&sign=Kvi47of0iu9L%2FPajfy%2F%2B3WsK4j2PwXR4H4Zw60LEYTJadv5wp1kXmzvbVFsf8p8gAgI%3D&sc=&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvkjVLKGx4OdIfhP9NU%2f21mFVTbdwKTuIC6ogKtzzr19pg%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
yule = 'http://iflow.uczzd.cn/iflow/api/v1/channel/179223212?app=ucnews-iflow&recoid=2471314011167358262&ftime=1539581070043&method=new&count=20&no_op=0&auto=1&content_ratio=0&_tm=1540307511754&sign=Kvgcty0GmntBeXUR6f83n2bOOluDnD4aRIIw%2Bm4rsLRaeuRwjgY1WFtvh5QbnIZtvWg%3D&sc=&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvnTtfl94gr0TscDiupliJZ%2baBoA1e70lfYHS4PTJd%2f9FQ%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
hulianwang = 'http://iflow.uczzd.cn/iflow/api/v1/channel/242677432?app=ucnews-iflow&recoid=&ftime=&method=new&count=20&no_op=0&auto=1&content_ratio=0&_tm=1540307534513&sign=KvhlMqOxdT1fcAtiEK62AM2Ag5vO44urtLUcyBP13VBxJBpU8i%2Bt2cVMn0H6bTb3hkI%3D&sc=&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvnTtfl94gr0TscDiupliJZ%2baBoA1e70lfYHS4PTJd%2f9FQ%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
qiche = 'http://iflow.uczzd.cn/iflow/api/v1/channel/323644874?app=ucnews-iflow&recoid=&ftime=&method=new&count=20&no_op=0&auto=1&content_ratio=0&_tm=1540307573532&sign=Kvgg3V1xhb3zPdfwrYqWFAbFVKyJEotauxcW3o%2BxYdKF5eQZr9IUUX%2FowD0%2FkqkUiTY%3D&sc=&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvnTtfl94gr0TscDiupliJZ%2baBoA1e70lfYHS4PTJd%2f9FQ%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
junshi = 'http://iflow.uczzd.cn/iflow/api/v1/channel/1105405272?app=ucnews-iflow&recoid=6631382522325951662&ftime=1539581345807&method=new&count=20&no_op=0&auto=1&content_ratio=0&_tm=1540307595296&sign=KvhUI5YwtkY5n5nUOiH8IQF6v5%2FN9Y5rSfpI6yDAa3A4y5lTXnsGarRrm1zQSsbZr3s%3D&sc=&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvnTtfl94gr0TscDiupliJZ%2baBoA1e70lfYHS4PTJd%2f9FQ%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
youxi = 'vhttp://iflow.uczzd.cn/iflow/api/v1/channel/169476544?app=ucnews-iflow&recoid=&ftime=&method=new&count=20&no_op=0&auto=1&content_ratio=0&_tm=1540307648300&sign=Kviy78X%2B1wYDSD0O7LbdCV9eZWFEx7ZVWfbQsMwpBMBWrW7X%2FNfxH4EeZM0VxkvoaHI%3D&sc=&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvnTtfl94gr0TscDiupliJZ%2baBoA1e70lfYHS4PTJd%2f9FQ%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
lishi = 'http://iflow.uczzd.cn/iflow/api/v1/channel/701104723?app=ucnews-iflow&recoid=11512934822734291305&ftime=1539580962937&method=new&count=20&no_op=0&auto=1&content_ratio=0&_tm=1540307679339&sign=KvjeR6Kc8%2FDwtNkToTdPCxMcacNlVf4wCH%2B3o8EcsnRGqGYjeJe8LM9TognxAZBG1fI%3D&sc=&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvnTtfl94gr0TscDiupliJZ%2baBoA1e70lfYHS4PTJd%2f9FQ%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
tiyu = 'http://iflow.uczzd.cn/iflow/api/v1/channel/923258246?app=ucnews-iflow&recoid=17112109162432428835&ftime=1540307710072&method=new&count=20&no_op=0&auto=0&content_ratio=0&_tm=1540308993602&sign=Kvg5w8p9ZdVOvg7nbQL2P3KdtMka8OCnFTnJnxJyZ9osukfy4STbCB6zpCEgBGRIqJ4%3D&sc=&uicid=KviA1sVwSNVrHokKYAqzFNDW0%2BSnKSS5ZikBmQpl1U6MAYtvvwpN6PjEF1CKJtvjZJs%3D&uc_param_str=dnnivebichfrmintcpgieiwidsudsvadmeprpf&dn=37016348931-02193660&nn=KvmoP3iY%2fiscv2pyDTljVgW9aWBGHs%2bn5J33OFV%2beQavPQ%3d%3d&ve=3.9.2.392&bi=997&ch=&fr=iphone&mi=iPhone9%2c2&nt=2&pc=KvmV1x3IdVeVUcW4KYHoQ%2f0%2b4%2bELgX3j0LxeHwNQoGBLaEFyhqeiySP3D2pMuhpGaAs%3d&gp=KvkDyr99TyLHftAL4ZaULwdm8lZ3cwzhBG9LNIjgiTymkw%3d%3d&me=KvlA4a0OFmlREej9Uhw8RvIHvr26EUScdveIfpXANTf%2fHRFc398pbEnFU%2bq9XS95Fso%3d&wf=&ut=KvnEckifrXQ3BPlsuBB1GgUgQEg%2bgWkB09rfM2unYZ3V%2bQ%3d%3d&ai=Kvk%3d&sv=app&ad=&pr=UCNewsApp&pf=195'
# type gaoxiao keji tiyu yule lishi junshi sannong meishi qiwen qiche xinlixue youxi redian
map = {'yule':yule,'hulianwang':hulianwang,'gaoxiao':gaoxiao,'keji':keji,'tiyu':tiyu,'lishi':lishi,'junshi':junshi,'qiche':qiche,'youxi':youxi}

db = getdb()
driver = webdriver.Chrome()

for index in range(1, 20000):
    for type, url in map.items():
        data = json.loads(requests.get(url).content.decode('utf-8'))['data']
        items = data['items']
        for item in items:
            article = data[item['map']][item['id']]
            zzd_url = article['zzd_url']
            title = article['title']
            view_cnt = article['view_cnt']
            if view_cnt > 5000:
                driver.get(zzd_url)
                time.sleep(3)
                source = driver.page_source
                divs = etree.HTML(source).xpath('//*[@id="contentShow"]/*')
                txt = []
                for div in divs:
                    text = div.xpath('./text()')
                    src = div.xpath('./img/@data-src')
                    if len(src) > 0:
                        txt.append(src[0])
                        txt.append('\n')
                        continue
                    if len(text) > 0:
                        txt.append(text[0])
                        txt.append('\n')

                # save_db(db, title=title, intro=introduction, type=k, cover=cover_all, content=''.join(txt),
                #         url=share_url, play=read_count, author=data['nickname'], author_img=data['avatar'],
                #         data=time.strftime("%Y/%m/%d %H:%M", time.localtime(data['show_time'])))
                # save_db(db, md5=md5, title=title, url=mp4_src, cover=article['thumbnails'][0]['url'], play=view_cnt,
                #         comment_url=article['cmt_url'], author=article['site_logo']['desc'], type=k,
                #         author_img=article['site_logo']['img']['url'],
                #         data=time.strftime("%Y/%m/%d %H:%M", time.localtime(int(article['grab_time'] / 1000))))