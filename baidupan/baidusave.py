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
from urllib.parse import unquote

from baidupan.ResultThread import ResultThread

sys.setrecursionlimit(1000000)  # 例如这里设置为一百万

cookie = ''
share_header = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Referer': 'https://pan.baidu.com/disk/home',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': cookie}

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
    'Cookie': cookie}


def net_post(url, data=None, json=None, **kwargs):
    print(unquote(url))
    print(data)
    result = requests.post(url, data=data, headers=create_header, verify=False).content.decode('utf-8')
    print(result)
    return result


def net_get(url, params=None, **kwargs):
    print(unquote(url))
    result = requests.get(url, headers=share_header, verify=False).content.decode('utf-8')
    print(result)
    return result


def shareMap(file={}):
    share_list = F'https://pan.baidu.com/share/list?uk={from_uk}&shareid={shareid}&order=other&desc=1&showempty=0&web=1&page=1&num=100&dir={file["filePath"]}&t={random.random()}&channel=chunlei&web=1&app_id={app_id}&bdstoken={bdstoken}&logid={str(base64.b64encode(str(time.time()*10000).encode("utf-8")),"utf-8")}&clienttype=0'
    all_file(share_list, file, 'share')
    return file


def myMap(file={}):
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
    shareFile = net_get(url)
    if len(shareFile) < 2:
        retry += 1
        if retry > 5:
            return None
        return file_get(url, retry)
    shareFile = shareFile[shareFile.index('{'):len(shareFile)]
    loads = json.loads(shareFile)
    if loads['errno'] != 0:
        retry += 1
        if retry > 5:
            return None
        return file_get(url, retry)
    return loads


def create_path(path, retry=0):
    create_url = F'https://pan.baidu.com/api/create?a=commit&channel=chunlei&web=1&app_id={app_id}&bdstoken={bdstoken}&logid={str(base64.b64encode(str(time.time()*10000).encode("utf-8")),"utf-8")}&clienttype=0'
    param = {'path': unquote(path), 'isdir': '1', 'block_list': []}
    result = net_post(create_url, data=param)
    if len(result) < 2:
        retry += 1
        if retry > 5:
            return
        create_path(path, retry)
    result = result[result.index('{'):len(result)]
    if json.loads(result)['errno'] != 0:
        retry += 1
        if retry > 10:
            return
        create_path(path, retry)


def transfer_file(path, fsid, type='', retry=0):
    if type == 'private':
        url = F'https://pan.baidu.com/mbox/msg/transfer?bdstoken={bdstoken}&channel=chunlei&web=1&app_id={app_id}&logid={str(base64.b64encode(str(time.time()*10000).encode("utf-8")),"utf-8")}&clienttype=0'
        param = {'from_uk': from_uk, 'to_uk': to_uk, 'msg_id': msg_id, 'ondup': 'newcopy', 'async': '1', 'type': '1',
                 'fs_ids': F'[{fsid}]', 'path': unquote(path)}
    else:
        url = F'https://pan.baidu.com/share/transfer?shareid={shareid}&from={from_uk}&ondup=newcopy&async=1&channel=chunlei&web=1&app_id={app_id}&bdstoken={bdstoken}&logid={str(base64.b64encode(str(time.time()*10000).encode("utf-8")),"utf-8")}&clienttype=0'
        param = {'fsidlist': F'[{fsid}]', 'path': unquote(path)}
    result = net_post(url, data=param)
    if len(result) < 2:
        retry += 1
        if retry > 5:
            return
        time.sleep(2)
        transfer_file(path, fsid, type, retry)
    result = result[result.index('{'):len(result)]
    if json.loads(result)['errno'] != 0:
        retry += 1
        if retry > 10:
            print(path)
            print(fsid)
            return
        transfer_file(path, fsid, type, retry)


def transfer(share={}, my={}, type=''):
    temp = False
    file_name = share['fileName']
    for sub in my['subFile']:
        if sub['fileName'] == file_name:
            temp = True
            break
    if share['isdir'] and str(file_name).find('kjdog') < 0:
        if not temp:
            create_path(F"{my['filePath']}/{file_name}")
            subFile = {'subFile': []}
            subFile['fileName'] = file_name
            subFile['filePath'] = F"{my['filePath']}/{file_name}"
            subFile['isdir'] = True
            my['subFile'].append(subFile)
        tsub = {}
        for msub in my['subFile']:
            if msub['fileName'] == file_name:
                tsub = msub
                break
        for sub in share['subFile']:
            transfer(sub, tsub, type)
    elif not share['isdir'] and str(file_name).find('kjdog') < 0:
        if not temp:
            transfer_file(my['filePath'], share['fs_id'], type)
    else:
        print('会计狗狗广告')


def refresh_header():
    global share_header
    share_header = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Referer': 'https://pan.baidu.com/disk/home',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookie}

    global create_header
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
        'Cookie': cookie}


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


def d2y():
    global cookie
    cookie = 'BIDUPSID=DC7BBC3BF80F0B4D394DD93F2BB79D54; PSTM=1481187061; panlogin_animate_showed=1; bdshare_firstime=1492834081929; PANWEB=1; __cfduid=d883c5690f8d164a8ffb5fc98785afea01532575554; MCITY=-%3A; BAIDUID=6EF572039DBDE67795CA0B1D3B168F3D:FG=1; H_PS_PSSID=; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1541948594,1542013530,1542180545,1542246294; Hm_lvt_407473d433e871de861cf818aa1405a1=1541948611,1542013539,1542180550,1542246299; BDCLND=pRaLQnlGJqNsvwZAKqL2EH7DRGrpwmco; delPer=0; PSINO=1; cflag=15%3A3; BDRCVFR[92PNfpaJZ0Y]=9xWipS8B-FspA7EnHc1QhPEUf; BDUSS=0gzM0h0Q1Z2ak9FenVScUZwUkh-eWhSSHlHNTVCWGZ-Nm5VVnM1bkN3WUlKQmRjQVFBQUFBJCQAAAAAAAAAAAEAAABjkWjP1LW31rPJzqrO0sPHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAiX71sIl-9bT; STOKEN=c8082eeecc1494189cfd4cc15a0a8236254ecbcbaec36e186c601dbec4a20897; SCRC=fe4c967d0a71f9a47ee5058a406cf0cf; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1542431997; Hm_lpvt_407473d433e871de861cf818aa1405a1=1542432003; BDRCVFR[jFeE7wK4p0D]=9xWipS8B-FspA7EnHc1QhPEUf; PANPSC=9211934974791907903%3AZjFd1PuLJ%2BAaQ5XmsatCaOn90oj%2BY%2FIsHJlweUJ02t1m1RVC%2Fg0eFdN%2Fz3Y2D0lvoJhNDqeencuFv6WU4Zl3wBOAD5r1J1nb%2B6ivvb20zlSjJmZCwYXPzsv%2BltDwt9lVNIE1TQmpy4bYFdTZP%2BpAvCtY6oDerc8JwO6IUlyEdXI5u4Owi7HyOET6EtWQMy2KSSzrHYofj1Q%3D'
    global bdstoken
    bdstoken = 'eb003277cc71a9106d0c9cb60278d212'
    global msg_id
    msg_id = '3350045725085442145'
    global from_uk
    from_uk = '2498556534'
    global to_uk
    to_uk = '2446011831'
    global fromFileName
    fromFileName = '2019初级职称'
    global fromFilePath
    fromFilePath = '/我的资源/2019全程备考包/2019初级职称'
    global fs_id
    fs_id = '828080111320777'
    refresh_header()
    from_map = {'fileName': fromFileName, 'filePath': quote(fromFilePath), 'isdir': True, 'fs_id': fs_id, 'subFile': []}
    from_thread = ResultThread(name='来源线程', target=privateMap, args=from_map)
    from_thread.setDaemon(True)
    from_thread.start()
    to_map = {'fileName': toFileName, 'filePath': quote(toFilePath), 'isdir': True, 'subFile': []}
    to_thread = ResultThread(name='我的线程', target=myMap, args=to_map)
    to_thread.setDaemon(True)
    to_thread.start()

    from_thread.join()
    to_thread.join()

    transfer(from_map, to_map, 'private')


def y21():
    global cookie
    cookie = 'BIDUPSID=DC7BBC3BF80F0B4D394DD93F2BB79D54; PSTM=1481187061; panlogin_animate_showed=1; bdshare_firstime=1492834081929; PANWEB=1; __cfduid=d883c5690f8d164a8ffb5fc98785afea01532575554; BAIDUID=6EF572039DBDE67795CA0B1D3B168F3D:FG=1; MCITY=-332%3A; recommendTime=guanjia2018-12-3%2010%3A40%3A00; BDCLND=OmNRaxsh%2BtndVBHLIC1IKCkwudPWE5%2BtgiTav7qXkrY%3D; H_PS_PSSID=; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1543912725,1544164837,1544173504,1544328791; Hm_lvt_407473d433e871de861cf818aa1405a1=1543901418,1544164844,1544173514,1544328797; delPer=0; PSINO=2; cflag=15%3A3; BDUSS=VzUU1ITFRhfjBBSjVpMUtRRTFCOVZTUEszMkdZSU9xNEpWVzgtN1JYZ2FmRFZjQVFBQUFBJCQAAAAAAAAAAAEAAACSAJzHuf7gtjIzNDU2tcS80gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABrvDVwa7w1ccU; STOKEN=cf740039fcb127c92ab233ad5d193f7866a20ce46dfd97c65319098d3ef98337; SCRC=cd71ed5a4323a80e4d7b4057bad4e589; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1544417055; PANPSC=8062411856976849230%3A5Us%2BCrpocqOKWrat4M8x7kvCu2t54Rp49SFoCO5trOtX8ZWcAfekebAEEJKb92oSDbk8E8gdDB%2BDOi2vRG4L0VLo%2FsO9TsywAJXi526GvO3eC2aLH2G6goSZYuWca%2FNU%2FPW39XmLfA94%2B2HacCA3yTsuktMw6gulbVFcNkn0FT5VvmSKYmKRhKQRuwhxVv30; Hm_lpvt_407473d433e871de861cf818aa1405a1=1544417061'
    global bdstoken
    bdstoken = 'b520a4d0e971675398d8b7e74aa985c5'
    global msg_id
    msg_id = '885630743877066688'
    global from_uk
    from_uk = '2446011831'
    global to_uk
    to_uk = '12835907'
    global fromFileName
    fromFileName = '2019初级职称'
    global fromFilePath
    fromFilePath = '/2019初级职称'
    global fs_id
    fs_id = '416989081489113'
    refresh_header()
    from_map = {'fileName': fromFileName, 'filePath': quote(fromFilePath), 'isdir': True, 'fs_id': fs_id, 'subFile': []}
    from_thread = ResultThread(name='来源线程', target=privateMap, args=from_map)
    from_thread.setDaemon(True)
    from_thread.start()
    to_map = {'fileName': toFileName, 'filePath': quote(toFilePath), 'isdir': True, 'subFile': []}
    to_thread = ResultThread(name='我的线程', target=myMap, args=to_map)
    to_thread.setDaemon(True)
    to_thread.start()

    from_thread.join()
    to_thread.join()

    transfer(from_map, to_map, 'private')



d2y()
y21()
