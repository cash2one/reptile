#!/usr/bin/env python
# encoding: utf-8
#   @file: baidusave.py
#   @Created by shucheng.qu on 2018/11/16
import os
import random

from selenium import webdriver
import json

import requests
from lxml import etree
import datetime
import time
import base64
import sys
from urllib.parse import quote

sys.setrecursionlimit(1000000)  # 例如这里设置为一百万

yuan17636 = 'BIDUPSID=DC7BBC3BF80F0B4D394DD93F2BB79D54; PSTM=1481187061; panlogin_animate_showed=1; bdshare_firstime=1492834081929; PANWEB=1; __cfduid=d883c5690f8d164a8ffb5fc98785afea01532575554; MCITY=-%3A; BAIDUID=6EF572039DBDE67795CA0B1D3B168F3D:FG=1; H_PS_PSSID=; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1541948594,1542013530,1542180545,1542246294; Hm_lvt_407473d433e871de861cf818aa1405a1=1541948611,1542013539,1542180550,1542246299; BDCLND=pRaLQnlGJqNsvwZAKqL2EH7DRGrpwmco; delPer=0; PSINO=1; cflag=15%3A3; BDRCVFR[92PNfpaJZ0Y]=9xWipS8B-FspA7EnHc1QhPEUf; BDUSS=0gzM0h0Q1Z2ak9FenVScUZwUkh-eWhSSHlHNTVCWGZ-Nm5VVnM1bkN3WUlKQmRjQVFBQUFBJCQAAAAAAAAAAAEAAABjkWjP1LW31rPJzqrO0sPHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAiX71sIl-9bT; STOKEN=c8082eeecc1494189cfd4cc15a0a8236254ecbcbaec36e186c601dbec4a20897; SCRC=fe4c967d0a71f9a47ee5058a406cf0cf; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1542431997; Hm_lpvt_407473d433e871de861cf818aa1405a1=1542432003; BDRCVFR[jFeE7wK4p0D]=9xWipS8B-FspA7EnHc1QhPEUf; PANPSC=9211934974791907903%3AZjFd1PuLJ%2BAaQ5XmsatCaOn90oj%2BY%2FIsHJlweUJ02t1m1RVC%2Fg0eFdN%2Fz3Y2D0lvoJhNDqeencuFv6WU4Zl3wBOAD5r1J1nb%2B6ivvb20zlSjJmZCwYXPzsv%2BltDwt9lVNIE1TQmpy4bYFdTZP%2BpAvCtY6oDerc8JwO6IUlyEdXI5u4Owi7HyOET6EtWQMy2KSSzrHYofj1Q%3D'
qu15380 = 'BIDUPSID=DC7BBC3BF80F0B4D394DD93F2BB79D54; PSTM=1481187061; panlogin_animate_showed=1; bdshare_firstime=1492834081929; PANWEB=1; __cfduid=d883c5690f8d164a8ffb5fc98785afea01532575554; MCITY=-%3A; BAIDUID=6EF572039DBDE67795CA0B1D3B168F3D:FG=1; BDUSS=VxdH5wcU5LNFlELUVUY0I5WnRiOTZkSlZLd2tlZGJQeFItaXg2OXhSQmY3TmRiQUFBQUFBJCQAAAAAAAAAAAEAAAAHBBkv0KHR-cTju7nMq8TbAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF9fsFtfX7BbOH; SCRC=65c922f050032feda5c5c729a7ef0491; H_PS_PSSID=; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1541948594,1542013530,1542180545,1542246294; Hm_lvt_407473d433e871de861cf818aa1405a1=1541948611,1542013539,1542180550,1542246299; BDCLND=Oclth5FfAbzXUX6tTlln03RxwXA6SBpy7yF%2FbLzUCrE%3D; STOKEN=e5b72022faf19e1a900bbdb45dad5bbee5bc8ba329506f79e421cd3d02e5198e; delPer=0; PSINO=2; cflag=15%3A3; Hm_lpvt_407473d433e871de861cf818aa1405a1=1542353652; PANPSC=17218965739127024165%3AM3%2Fm2%2F8VCaBbxK%2FYR74R10vCu2t54Rp4tNz8gfJx91ehClz94JG8KvkEtsZJBi2OtwQSqriNDotQXOzmXp7MaHgXofrWESI40Kx5odaStsWXc8ySyDMeokNCOFfstLl9CFXShhl2gVitUq%2FdzxBw4g%2BV45jZmyoa%2F1txkewJEk0nih65clERtryHDAnhPhMz5dNt%2BsRbU69UMSLhYBPCxc5TMpqnKCFM; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1542353829'
share_header = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Referer': 'https://pan.baidu.com/disk/home',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': yuan17636}

create_header = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'https://pan.baidu.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://pan.baidu.com/disk/home',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': yuan17636}


def shareMap(file={}):
    share_list = F'https://pan.baidu.com/share/list?uk={from_uk}&shareid={shareid}&order=other&desc=1&showempty=0&web=1&page=1&num=100&dir={file["filePath"]}&t={random.random()}&channel=chunlei&web=1&app_id={app_id}&bdstoken={bdstoken}&logid={str(base64.b64encode(str(time.time()*10000).encode("utf-8")),"utf-8")}&clienttype=0'
    all_file(share_list, file, 'share')
    return file


def myMap(file={}):
    # my_list = F'https://pan.baidu.com/api/list?dir={file["filePath"]}&bdstoken={bdstoken}&logid={str(base64.b64encode(str(time.time()*10000).encode("utf-8")),"utf-8")}&num=100&order=time&desc=1&clienttype=0&showempty=0&web=1&page=1&channel=chunlei&web=1&app_id={app_id}'
    my_list = F'https://pan.baidu.com/api/list?order=time&desc=1&showempty=0&web=1&page=1&num=100&dir={file["filePath"]}&t={random.random()}&channel=chunlei&web=1&app_id={app_id}&bdstoken={bdstoken}&logid={str(base64.b64encode(str(time.time()*10000).encode("utf-8")),"utf-8")}&clienttype=0&startLogTime={int(round(time.time()*1000))}'
    all_file(my_list, file, 'my')
    return file


def privateMap(file={}):
    private_url = F'https://pan.baidu.com/mbox/msg/shareinfo?msg_id={msg_id}&page=1&from_uk={from_uk}&to_uk={to_uk}&type=1&fs_id={file["fs_id"]}&num=50&bdstoken={bdstoken}&channel=chunlei&web=1&app_id={app_id}&logid={str(base64.b64encode(str(time.time()*10000).encode("utf-8")),"utf-8")}&clienttype=0'
    all_file(private_url, file, 'private')
    return file


def all_file(url, file={}, type=''):
    loads = file_get(url)
    if type == 'private':
        lists = loads['records']
    else:
        lists = loads['list']
    for item in lists:
        filePath = item['path']
        fileName = item['server_filename']
        isdir = item['isdir']
        fs_id = item['fs_id']
        subFile = {'subFile': []}
        subFile['fileName'] = fileName
        subFile['filePath'] = quote(filePath)
        subFile['fs_id'] = fs_id
        subFile['isdir'] = isdir == 1
        file['subFile'].append(subFile)
        if subFile['isdir']:
            if type == 'my':
                myMap(subFile)
            elif type == 'share':
                shareMap(subFile)
            elif type == 'private':
                privateMap(subFile)


def file_get(url, retry=0):
    shareFile = requests.get(url, headers=share_header, verify=False).content.decode('utf-8')
    time.sleep(1)
    shareFile = shareFile[shareFile.index('{'):len(shareFile)]
    loads = json.loads(shareFile)
    if loads['errno'] != 0:
        retry += 1
        if retry > 5:
            return None
        file_get(url, retry)
    return loads


def create_path(path, retry=0):
    create_url = F'https://pan.baidu.com/api/create?a=commit&channel=chunlei&web=1&app_id={app_id}&bdstoken={bdstoken}&logid={str(base64.b64encode(str(time.time()*10000).encode("utf-8")),"utf-8")}&clienttype=0'
    param = {'path': path, 'isdir': '1', 'block_list': []}
    result = requests.post(create_url, data=param, headers=create_header, verify=False).content.decode('utf-8')
    time.sleep(1)
    if json.loads(result)['errno'] != 0:
        retry += 1
        if retry > 10:
            return
        create_path(path, retry)


def transfer_file(path, fsid, type='', retry=0):
    if type == 'private':
        url = F'https://pan.baidu.com/mbox/msg/transfer?bdstoken={bdstoken}&channel=chunlei&web=1&app_id={app_id}&logid={str(base64.b64encode(str(time.time()*10000).encode("utf-8")),"utf-8")}&clienttype=0'
        param = {'from_uk': from_uk, 'to_uk': to_uk, 'msg_id': msg_id, 'ondup': 'newcopy', 'async': '1', 'type': '1',
                 'fs_ids': F'[{fsid}]', 'path': path}
    else:
        url = F'https://pan.baidu.com/share/transfer?shareid={shareid}&from={from_uk}&ondup=newcopy&async=1&channel=chunlei&web=1&app_id={app_id}&bdstoken={bdstoken}&logid={str(base64.b64encode(str(time.time()*10000).encode("utf-8")),"utf-8")}&clienttype=0'
        param = {'fsidlist': F'[{fsid}]', 'path': path}
    result = requests.post(url, data=param, headers=create_header, verify=False).content.decode('utf-8')
    time.sleep(1)
    print(result)
    if json.loads(result)['errno'] != 0:
        retry += 1
        if retry > 10:
            print(path)
            print(fsid)
            return
        transfer_file(path, fsid, type, retry)


def transfer(share={}, my={}, type=''):
    if share['isdir']:
        file_name = share['fileName']
        temp = False
        for sub in my['subFile']:
            if sub['fileName'] == file_name:
                temp = True
                break
        if not temp:
            create_path(F"{my['filePath']}/{file_name}")
            subFile = {'subFile': []}
            subFile['fileName'] = file_name
            subFile['filePath'] = F"{my['filePath']}{file_name}/"
            subFile['isdir'] = True
            my['subFile'].append(subFile)
        for sub in share['subFile']:
            for msub in my['subFile']:
                if msub['fileName'] == file_name:
                    transfer(sub, msub, type)
                    break
    else:
        transfer_file(my['filePath'], share['fs_id'], type)


# share_map = shareMap({'fileName': fileName, 'filePath': filePath, 'isdir': True, 'subFile': []})
# my_map = myMap({'fileName': '', 'filePath': '/', 'isdir': True, 'subFile': []})
# transfer(share_map,my_map)

toFileName = ''
toFilePath = '/'
shareid = '1349087131'
app_id = '250528'
bdstoken = 'eb003277cc71a9106d0c9cb60278d212'
msg_id = '3350045725085442145'
from_uk = '2498556534'
to_uk = '2446011831'

fromFileName = '2019全程备考包'
fromFilePath = '/我的资源/2019全程备考包'
fs_id = '386526453858121'

from_map = privateMap(
    {'fileName': fromFileName, 'filePath': quote(fromFilePath), 'isdir': True, 'fs_id': fs_id, 'subFile': []})
to_map = myMap({'fileName': toFileName, 'filePath': quote(toFilePath), 'isdir': True, 'subFile': []})
transfer(from_map, to_map, 'private')

# print(json.dumps(myMap({'fileName': '', 'filePath': '/', 'isdir': True, 'subFile': []})))
# print(create_path('/这个是测试目录'))

# transfer_file('/','611687935140417')
