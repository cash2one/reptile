#!/usr/bin/env python
# encoding: utf-8
#   @file: qttmp4.py
#   @Created by shucheng.qu on 2018/10/5

import json

import requests
from lxml import etree
import datetime
import time
from urllib.parse import unquote
from newreptile.utils.dirs import makedirs
from newreptile.utils.save import save
from newreptile.xigua.xgupload import upload


url = 'https://api.1sapp.com/content/getListV2?qdata=MzEwRTU4RjM3MDFFMTg0MEM2OTQ3NkRFN0FFRkRGRjguY0dGeVlXMGZSREV4TkRoQk4wRXRPVEV4TWkwME5URkZMVUZETVVFdE5UWTJSa1V6T1VJMVFrWkZIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS6YZ7PdNB3DmKmXcuJHtev7Hk9IztIfaB77%2Bf9GdIpdLFJLzAl55DyM9XhwZf1YSR9iw11CIxvPpspHqbZrKw8C3WUUIIUjHZje4%2Bve6adhdVLZal0xRDjEqlTiADJ9yG0fBVVShxLxJJgDXjMUHJ1qRD52vGXXOwKjh1thZV9ommcvq3bB/2x/2zvmhUWLOGIi94afKzoj/4mgZNuwVTgHk2c99MHeran/Es5DkOLX3jsjWLVwpOMTp/tDe9DF/cgL2tszGa7SYiL66Dx6HjJ%2BSDgeVPbbFhxTeX91dUMKcVdUPkyLLVw/obLkjNyt46G6s%2BVZPC4%2Bxy5MWN6mrXHloZzPLWJyW3ik//N4FPXa%2BBlQKJyFCFJJ5K4KP031lMqJcpAZKNbWU95BAi5WLNUWNXUfFDTQZLFonHmtDnMq05YII1meFo%2BsaC9e5zyoAHIvwpcMpIhaR2imUlGXW%2BRAXvJT95G91chffpi/lgW/fzPS2dPSiWw03YESv2CnopErTXZohT/AfjQE2syF8zo6arEC/Jy8y1HYjjXJERP6sy6ky%2BOfbHLIZN9Y%2BaRisCSlsxF577a3WT%2B8XpwRdtdg26uuV9VsesfYuPNRYRQmB6O4q3tRmVxavmuUzmSTXF3GfpwDxAIQBvfknApdG9ESmOExzwQbzQAZPeHT1D%2BdlRBnN63rod1JUqwnQ5W%2B4b2d4DPkOq12d8seL0cvc3/tXRhVwNpjnDtJvge5QhW4U/MP7ebL8I5MltsGa56Za/37WJHS597R/Oee2/HG9La3BVityQi29EDJpIruHmB/DrI%3D'

path = makedirs('qutoutiao', 'qiwen')
for index in range(1,200):
    content = requests.get(url).content.decode('utf-8')
    data = json.loads(content)['data']['data']
    for da in data:
        try:
            read_count = int(da['read_count'])
            if read_count > 50000:
                read_count = int(read_count/10000)
                title = da['title']
                src = da['video_info']['hd']['url']
                print(f'{read_count}    {title}     {src}')
                name_path = f'{path}/{title}{read_count}.mp4'
                save(name_path,src)
                upload(name_path)
        except Exception as e:
            print('爬到一条广告，跳过去')
    print(f'趣头条视频    爬虫第 {index} 页完成')