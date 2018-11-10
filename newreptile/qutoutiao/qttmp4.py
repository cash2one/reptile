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
from newreptile.xigua.xgupload import upload, uploadBr

# url = 'https://api.1sapp.com/content/getListV2?qdata=MzEwRTU4RjM3MDFFMTg0MEM2OTQ3NkRFN0FFRkRGRjguY0dGeVlXMGZSREV4TkRoQk4wRXRPVEV4TWkwME5URkZMVUZETVVFdE5UWTJSa1V6T1VJMVFrWkZIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS6YZ7PdNB3DmKmXcuJHtev7Hk9IztIfaB77%2Bf9GdIpdLFJLzAl55DyM9XhwZf1YSR9iw11CIxvPpspHqbZrKw8C3WUUIIUjHZje4%2Bve6adhdVLZal0xRDjEqlTiADJ9yG0fBVVShxLxJJgDXjMUHJ1qRD52vGXXOwKjh1thZV9ommcvq3bB/2x/2zvmhUWLOGIi94afKzoj/4mgZNuwVTgHk2c99MHeran/Es5DkOLX3jsjWLVwpOMTp/tDe9DF/cgL2tszGa7SYiL66Dx6HjJ%2BSDgeVPbbFhxTeX91dUMKcVdUPkyLLVw/obLkjNyt46G6s%2BVZPC4%2Bxy5MWN6mrXHloZzPLWJyW3ik//N4FPXa%2BBlQKJyFCFJJ5K4KP031lMqJcpAZKNbWU95BAi5WLNUWNXUfFDTQZLFonHmtDnMq05YII1meFo%2BsaC9e5zyoAHIvwpcMpIhaR2imUlGXW%2BRAXvJT95G91chffpi/lgW/fzPS2dPSiWw03YESv2CnopErTXZohT/AfjQE2syF8zo6arEC/Jy8y1HYjjXJERP6sy6ky%2BOfbHLIZN9Y%2BaRisCSlsxF577a3WT%2B8XpwRdtdg26uuV9VsesfYuPNRYRQmB6O4q3tRmVxavmuUzmSTXF3GfpwDxAIQBvfknApdG9ESmOExzwQbzQAZPeHT1D%2BdlRBnN63rod1JUqwnQ5W%2B4b2d4DPkOq12d8seL0cvc3/tXRhVwNpjnDtJvge5QhW4U/MP7ebL8I5MltsGa56Za/37WJHS597R/Oee2/HG9La3BVityQi29EDJpIruHmB/DrI%3D'

# path = makedirs('qutoutiao', 'qiwen')

redian = 'https://api.1sapp.com/content/getListV2?qdata=Q0VBNzA0NEE4RkJGNDdENkM4MEZFQkJCMkQ5NTRCQUUuY0dGeVlXMGZOVFUyTURRd1FqQXRNa1pHUmkwMFFVWkdMVUV6TTBVdE1rTTJSREJDTUVOQlEwVkNIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS66sPI1fml7cHR0oFaU6111sI91ueBp0lfFqiSEtDlDTApL7kgMncbc8iJ6Y1bhb6a0GoyC/BX0cqILV4jTfY09biERW4JpVpd/SAHVdW5UnHeOueilEAohkSlavgPnDaY/Mn%2Bm/1sE5Qb6bEg9w/LpQflCAjGVXOBonfm3TPyHuKSWfRt7I6Gh6FsAiOh/0u9LwOMjs3RgDNav%2BnzZJEqRa8J71RDA%2BInhl2XQydSMJJPldqI4lgnQkJhj6sex%2B5MiRr2acCYFFqdKJOAGgwVv/Wp7vqRiOQ%2BN1BaZcBds8CzWkG7QNxEVoG1hVZG7AswTmLfN/bTduZTNS/yNCeJu7h6gC0NrHFbOc08vP2EPTA9oAuO2pKKqIep6EhMHKC28EQ6%2BBbOBYdswwBSYujS7qrvEiJRYO7buV1ORZaokrHicln/3YqyRFHguZTFvFSYzGdQN5hIvKKs7XSpENNK/TT5/tKxout/iEiWE/ueAY3Sbh3tBHctOQgL0NLNrsKIwjCk7CzFiouu44l8L0T53eaFCAH3DjOMboC3x7x/wqVdm3Z6aWqmSA7ps5/1ARVA9NNsYCN9yHe8vLf4pxC2XbuHWGummUJnhoLIsp71H8ZNgjv7MAYNGtQ3UKKC7IdcY9TMPzVVZYJj9qpPSn1FdVQ%3D%3D'
yule = 'https://api.1sapp.com/content/getListV2?qdata=OEM5OTlFNkFDODA2QTVEQ0Y5N0MxRTk2OEY0REIzMjIuY0dGeVlXMGZOa1UyTTBOQ05rRXRNVEU1TVMwME9EaEVMVUk0TjBFdE1qY3hOakEzUWpKQ1FVUTFIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS7ORXpIT8UhzS1qA4R0P5fRkNorS0Or%2B7UOk70eDQ3leBpzLV%2BOb9YRzPScbzqBNzeAaTFAKnEBeIm8J%2BhBUDvC2pYhNpgk1NBb9qjADKTosEMRlgNrSb8HhPzfEN%2BkFOKkHezwuf69bVyWHhrzX1dQNXAp3qLmbzklpG8OSuj9L3j5xb1YwfFyBp1y1uJRhQoQWaG4xiYqRpFGECB/PUMGghC8wXVN%2BI8AmQp9uqsnSbMhJCQHcQ8c4YLoFk3UJGL2siOvmTIGQFt%2Bp9I08BycJ7ynhqRfBetnjPTjOB0AYZwLXWVWwOP%2BDL%2BF%2Bph2flt9jrD8XOnOIxgk5G%2BaIfKdcez4nxNZQntbfXDgGngX6YrK6YzaUZmmrp1nb7lwx6JgTEBSfO7rCDWe9%2BFfISfekx%2BqVjNnOKQfqmxHVnZRbLvOp7/7zluZA8GG1dk3tRFZn1TEIWmBfBqwbi6zNeVIR8i9b9x1QyOib0jnemzC82Rw4ch9D0UGCIjRaRC8ZHXvj%2B6iW56qopXgROVmxt3NNHf1cdQ38eI78TkVX7L8z0pI6nuTfhAsmKHiSzCLc%2BjKd27Wsj%2BA47TkCJJv36ijgVI4M/5J3qgHhT5Xop9oAqwdliX8wdJwTMk2LtS1X0PC7AoO6iG6FLLvi%2BmxLLgFGA%3D%3D'
shenghuo = 'https://api.1sapp.com/content/getListV2?qdata=M0UxQTI0NDY5QzY1NDk1QkNENkE4RDkwQTVCRTlGNjguY0dGeVlXMGZNRFF3UlVVd1FrSXRRek0xUWkwME1EaEdMVUUyTWpZdE5qVTJRemhFTWpJMVJFTkdIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS5YlGg26rd1RQQn5VJw4aHFjOlrlS2swvr0cC%2Bih0Pf974M%2BuVaOoXbwWpwib/pU5G9Eh24E94JXyVmJyT0T3AYmENL2hg4QCVS5K4WWZhAh0RLt69LrLSt4jx%2BjXYwyaTFZQkvivXb2ocqSZLJNwOj931eSJXab/0%2B9iQvr4slckDpxfCvItTSUFgIP/R8b28C9b2Rbq9VvkjBcruSRaOxHbnrh1o0j3pKNWP3pHh170pLu07WwQcF%2BciBJg1OaOcgkZoeYjEoM3WSG5WMxW9AMGKm6bbtCXubLf3CeGWa19s6Jtc2FmXqJ6cdxnWoRWHCsrTD/S0gpi99hX2hFpcMsV9QhoLClo5mMGJSc82zyqF9eQsRqPrYGnKGLHOe7xCPOl2I6c%2B7a3JBSVI8LjcP7XfhlL2sC/a0bWSdAQPqgSN%2BDLeyZoat%2B9yokDtjD5zqenp5iRV4zBMAWHzcRsYgjnxA06njdzixZzB/yHoIXCGmGnVtVHNxhId3mDDGdyNXU4BEAuGk72VqvEZfcYkFFUOwwXSArRePce6mGLphCD%2B2%2BpdXUjKbepTmfRTnbGNfo5iwK5olQ20GjFU2HkUAVdGeG8JLjMAog5jYgvz1uk3/WzwK8CM5XAvyQMPpFH00N%2BI1O8i6SQgkKnQG5/C6BA%3D%3D'
qiwen = 'https://api.1sapp.com/content/getListV2?qdata=ODk2QUZCRTkwRDEwNUUwRTEzOUI3N0M3MkExMDUzODQuY0dGeVlXMGZOVFkyUTBNNE5UWXRNRUkzUVMwME1USXpMVGhCTmtFdE56YzFNall4TURZMU0wRkRIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS553B1FUdfifdpfzGa4okUAOJOTMAV%2BFmgs7E20K6G2nCGiMgkST1nPVZg4sZPJ5zew8A3wilE2h2Uyums2yciRSbmqutOuXVibthy6TnJQOolaEnWWwBmjQXVcV9lz8R2RLo2QUEk6sW5cEx2C1he%2By%2BpoXoDNq0OuEU%2BO26g1wjsY%2BpBei2cTlReaN9SU6mYQACA2zW2/umW9LL5sulDR87CusFrPwqoUCzfsp6I72eX00MKDnHgGMuNJvq5Fviv9NNNzAFtCVPlqkknYg7l7VhkKklezTjfTvH0zL%2BIICXNgEQSlLieUVJz91sssA60t38w46i%2BSOSKeYUcrDhfuGDiCL9Zr2cKiUTt47DhytAw%2Bwj5mbEbB01hD%2BAQZiTmov5CoCjG3spJRKP3Vpy7oB5d74RKqPizwZUgMraONWsj04W/KJKl1JBUVTCJXZdGcF5jm7Jq3hNnVzPSiT3/QSa43/77iA30ou8l9tnTARHfUWQwg%2BWNYeOSObSX6Vk1wyZncgZBmfCrKnw34Ldqsf%2BRAL4Od/5ZastMy0jMPhTIetZQWwROMDOZ639eEvATgzHGQGgp4S7JmJwBfWnD1SLtisL4bVwlopk/T6MKlObGnS3H2jvmTQTFsnHnjRH98i8%2B6IpstZY17EnOj2dpOmw%3D%3D'

tuijian = 'https://api.1sapp.com/content/getListV2?qdata=QTMwQjFDODQ0NjgxNUYyMTBBRTgxMEVBQTNCNDJGRUMuY0dGeVlXMGZORVF5T1RORk56UXRRekkwT1MwME9FVTBMVUpDT0RRdE1UQXlNVFF4TmtGRE5rSkVIblpsY25OcGIyNGZNaDV3YkdGMFptOXliUjlwYjNNPS752mSFJAeiqplZdNzNWbwM23DV%2BnNitl08epfx1TDgdsdCk8mPQhP0TG0SrYPctv7YiiuZ7Vsh60VtXY4HE71IfFAF%2BUp4NK0KLq34hkEJu4s6j1dphkzEyrc1uIxXGY9okJ9RscTRXTzZ8agbQciMnikxbK1TXlzvlSLf2ZCIg4xiX3q30bnSVlUGJKfkjdiitojC6ETfiF6hE4VGy5cWjc5hbp44nT%2BUyF6A8GYuREFJNvhMNe7dp2GnhtqdtiK8hbIr4pMzlswa%2BGJzgzVd%2BLjP6NrkOiT0ZkjoG1e/k0N3%2BQQNFEctfzcl/Ong/LMl6KUa5/JmKTAQE9aE65cM05pW7lJlv5W%2B9KW7cuKAeHIk%2BdKFkOknGtjPVgbGe3HOk9GlyWfr9NkfHTAB8KUDVlMaaOvHQlJ/gOqQIHI89tKexlwDam7VOBCp8Xp5KPccDVZcti2jsRUejJl%2BYufg1tonueK3JE0vSzhiYNM5WxN0KzzQc0Kx43pD2mpYoty9G/rW0Slp78YyBGzrXud/iwkuqjFMqJTDXEZQs2SLL2QY%2B3PR2SXFV1cJAwGChtSYbk2yulUXq8giVBJvDl8VMCifs473DW0HZP59L%2BfDvycZLpWV6XYphmf%2B6iOInjH%2BlIDkuo96OOYkn67zfGyqzN1VY5E7gu%2BF%2BrVkrQIvpRY%3D'

toutiao = {'video_society': redian, 'video_funny': qiwen}

for index in range(1, 2000000):
    for type, url in toutiao.items():
        content = requests.get(url).content.decode('utf-8')
        data = json.loads(content)['data']['data']
        for da in data:
            try:
                read_count = int(da['read_count'])
                if read_count > 50000:
                    # read_count = int(read_count/10000)
                    title = da['title']
                    src = da['video_info']['hd']['url']
                    print(f'{read_count}    {title}     {src}')
                    # name_path = f'{path}/{title}{read_count}.mp4'
                    # save(name_path,src)
                    # upload(name_path)
                    uploadBr(type, F'{title}.mp4', requests.get(src).content)
                    time.sleep(5)
            except Exception as e:
                print(e)
                print('爬到一条广告，跳过去')
        time.sleep(1)
        print(f'趣头条视频    爬虫 {type} 类型完成')
    print(f'趣头条视频    爬虫第 {index} 页完成')
    if index % 5 == 0:
        time.sleep(3 * 60 * 60)
