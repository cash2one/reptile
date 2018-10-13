#!/usr/bin/env python
# encoding: utf-8
#   @file: qttnews.py
#   @Created by shucheng.qu on 2018/10/10
import json
import time
from newreptile.utils.save import savenews
from newreptile.jinritoutiao.jrttnewsupload import upload_news
import requests
from lxml import etree

from newreptile.utils.dirs import makedirs

url = 'https://api.1sapp.com/content/getListV2?qdata=RUFEODFGQjBBMkY5RjRGRUFBMDk5RjRFREE4RTI5QzMuY0dGeVlXMGZSRGRHUmtJMk1EUXRRekJDUkMwME9EQkJMVUl4UWpFdE9FWTJSREJCUVVZNE9EUXpIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS6cnQPTmo4UjSjjHVUWEz/dv5YPSy4rvc5iVhH2MBc3pKjjm4xOhe%2BgA1WBIyklwnPT6gi/emFarE11slbxnOkHkOW5DX8mTQy/eHYWOOJXnp7NUMXJF98HmYgwIxEljt/Z%2Bp365yCqX6SNm2LjaX9XmY31PbTDecLycr6bMZORw9byqtBWd1CVkuDZMkE%2BArcUZ3VxpdRXphg226jAMwTHcZp34xNoWv6dbcO7j3YubTFikhe%2BT6qKbZn1rBtmSaQt0NaTsogwazSmGPrVZu8XnhCA5JZE%2BtmMVToMCyF3D6WRm9l4IKy0Vo%2BI4QxGQZPcTvitJJM1pOZaFDYnHp6wPOyQbaRNFKHsharQLEcrc17jCEakYKGO3e1O3dipFi9jANedWJRrapsSosxq0Rv/e7e8P4faDpRzdmRg3xviyG1XhUbGm0WhD2wV8Jw7VEfLRAsIJ9s%2BnYCjmeWyftq%2BMgYmULu5g/5dSeiO47PmOOZiDzx6qEhYCfZjnwRnU6S6igzmG1bV24Ag5CsWwb8IRWkojNMbmE0POK/fPg8hHUrgq5xoq%2B5sZ1xWogbd8UajX/G8b6ubrKQjdn/7hWeSzvWwiSTLWMUVXYHOmOP9uDs8nxpPgkFjQjMHqMcQdMeZuRxAlo3Tmb5LbPFZ037kWpPmTankZMRdjCrm1%2BjT7HkroQd0ZKc%2BjJ6NCDRaeNLR2j8cwsIGh1qKNJVs3YSNhTH2Mq4h0pf6%2BiJIshacRr7MvvzxPy%2BwWH8pVhk/nOtoaAEOF49V0fWvSoVK7uPN2uVtpXRsaxXCCBmU9YDfw/o%3D'
path = makedirs('news', 'qtt')
for index in range(1, 100):
    content = requests.get(url).content.decode('utf-8')
    datas = json.loads(content)['data']['data']
    print(content)
    for data in datas:
        try:
            # 文章url
            share_url = data['share_url']
            title = data['title']
            read_count = int(data['read_count'])
            if read_count < 1000:
                continue
            if not data['tips'] == '':
                continue
            print(F'{read_count}    {title}')
            # read_count = int(read_count/10000)
            # 简介
            introduction = data['introduction']
            news_content = requests.get(share_url).content.decode('utf-8')
            divs = etree.HTML(news_content).xpath('/html/body/section[1]/div/div[2]/p')
            txt = [F'title:{title}\n', F'introduction:{introduction}\n']
            for div in divs:
                text = div.xpath('./text()')
                src = div.xpath('./img/@data-src')
                if len(text) > 0:
                    txt.append(text[0])
                    txt.append('\n')
                if len(src) > 0:
                    txt.append(src[0])
                    txt.append('\n')
            path = F'{path}/{title}.txt'
            savenews(path,''.join(txt))
            upload_news(path)
        except Exception as e:
            print(e)
    time.sleep(5)
    print(F'趣头条 新闻爬虫 {index}    页完成！')
