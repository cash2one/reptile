#!/usr/bin/env python
# encoding: utf-8
#   @file: xgupload.py
#   @Created by shucheng.qu on 2018/10/8
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

cookie1 = 'UM_distinctid=16618b95ff8fec-0fa240b9021b02-346a7809-13c680-16618b95ff962c; ccid=296a02fee1cb2bde36141ce9b5fb805b; tt_webid=6605715939382117896; _mp_test_key_1=8c5ba2f4856e1f876d04252a1c8384a1; odin_tt=262ede1235a3aeabad5bf1c22afdcce2e084b30e253823fdf3ceff9e01357cc2c7669544ca3074e1a37bc85418daaa04; toutiao_sso_user=c74691eabf1d099ea05c0454cf743e59; sso_login_status=1; login_flag=ba6e0a6676bb4d786cfdb690ba7205ba; sessionid=44d6b943ce601a25e0ce8e16c35bed71; sid_tt=44d6b943ce601a25e0ce8e16c35bed71; sso_uid_tt=d34e114a7e1528a0672cad21666554ce; uid_tt=e811dd21e8eb1b56ce7fd04963da74ea; sid_guard="44d6b943ce601a25e0ce8e16c35bed71|1538033885|15552000|Tue\054 26-Mar-2019 07:38:05 GMT"; uuid="w:de2c0423770643e5a4cc4a740d70f61e"; __tea_sdk__ssid=beec8374-ce22-4c85-85e8-0c0ec8728c41; _ga=GA1.2.690585305.1538033999; _ba=BA0.2-20180927-5110e-7cBJlpop5WtJMqHFzCGe; _mp_auth_key=d371927ba601cd61df6662a833cedb0d; tt_im_token=1538561362991433327555356191813192730245609901956983232219431908; __tea_sdk__user_unique_id=104777979000; _ga=GA1.3.690585305.1538033999; __utma=24953151.690585305.1538033999.1538793328.1538793328.1; __utmz=24953151.1538793328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gid=GA1.2.781188670.1538911001; currentMediaId=1612724255524878; ptcn_no=6dbd2f538717f56aaa6e15126cb392e5'

cookie = 'UM_distinctid=16618b95ff8fec-0fa240b9021b02-346a7809-13c680-16618b95ff962c; ccid=296a02fee1cb2bde36141ce9b5fb805b; tt_webid=6605715939382117896; toutiao_sso_user=c74691eabf1d099ea05c0454cf743e59; uuid="w:de2c0423770643e5a4cc4a740d70f61e"; __tea_sdk__ssid=beec8374-ce22-4c85-85e8-0c0ec8728c41; _ga=GA1.2.690585305.1538033999; _ba=BA0.2-20180927-5110e-7cBJlpop5WtJMqHFzCGe; __tea_sdk__user_unique_id=104777979000; _ga=GA1.3.690585305.1538033999; __utma=24953151.690585305.1538033999.1538793328.1538793328.1; __utmz=24953151.1538793328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); odin_tt=89b29ff95caee0064fc3b71f1b077e8390234df5e61edd78c4111b4eff8cce5d909091651896c01d6022c9b65197e5f8; _mp_auth_key=fdc16d926f72be1d29d52e04ecd3f657; sso_uid_tt=a41eed69c2571e9256550216a1caf610; sso_login_status=1; _mp_test_key_1=a5b1e3c5d96eec58ea03a0532fef1c01; login_flag=6a574675b0249274fa298648af802d34; sessionid=1dfd03f6e2723d6e3231f09980e91236; sid_tt=1dfd03f6e2723d6e3231f09980e91236; sid_guard="1dfd03f6e2723d6e3231f09980e91236|1541860048|15552000|Thu\054 09-May-2019 14:27:28 GMT"; uid_tt=e5aab26106e9106c0bba3b6dc0e2d455; tt_im_token=1541860049794962701804000954053188567837980081810665939656178738; Hm_lvt_407473d433e871de861cf818aa1405a1=1541570146,1541859150,1541859190,1541860063; Hm_lpvt_407473d433e871de861cf818aa1405a1=1541860063; ptcn_no=3001a032b6ec69c5164a386036f63e6f'

headers = {
    'Connection': 'keep-alive',
    'Content-Length': '51',
    'Origin': 'https://mp.toutiao.com',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://mp.toutiao.com/profile_v3/xigua/upload-video',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': cookie}
if_headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://mp.toutiao.com/profile_v3/xigua/upload-video',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': cookie}

md5_headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.toutiao.com/profile_v3/xigua/upload-video',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': cookie}

up_headers = {
    'Connection': 'keep-alive',
    'Origin': 'https://mp.toutiao.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.toutiao.com/profile_v3/xigua/upload-video'
}
op_headers = {
    'Connection': 'keep-alive',
    'Access-Control-Request-Method': 'POST',
    'Origin': 'https://mp.toutiao.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Access-Control-Request-Headers': 'content-range',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'}
url = 'https://mp.toutiao.com/video/video_api/'


def upload(name_path):
    print(name_path)
    with open(name_path, 'rb') as file:
        try:
            read = file.read()
            md5 = hashlib.md5()
            md5.update(read)
            md5 = md5.hexdigest()
            md5_check = f'https://mp.toutiao.com/video/video_uniq_api/?md5={md5}'
            md5_content = requests.get(md5_check, headers=md5_headers, verify=False).content.decode('utf-8')
            is_uniq = json.loads(md5_content)['is_uniq']
            if not is_uniq:
                return
            split = str(name_path).split('/')
            name = split[len(split) - 1]
            params = {'json_data': '{"api":"chunk_upload_info"}'}
            content = requests.post(url, data=params, headers=headers, verify=False).content.decode('utf-8')
            print(content)
            up_date = json.loads(json.loads(content)['data'])
            upload_id = up_date['upload_id']
            upload_url = up_date['upload_url'].replace('http', 'https')
            lens = len(read)
            requests.options(upload_url, headers=op_headers, verify=False)
            up_headers['Content-Range'] = f'bytes 0-{lens-1}/{lens}'
            multipart_encoder = MultipartEncoder(
                fields={
                    'video_file': (name, open(name_path, 'rb'), 'application/octet-stream')
                },
                boundary='----WebKitFormBoundary' + str(random.randint(1e28, 1e29 - 1))
            )
            up_headers['Content-Type'] = multipart_encoder.content_type
            up_part = requests.post(upload_url, data=multipart_encoder, headers=up_headers,
                                    verify=False).content.decode(
                'utf-8')
            print(up_part)
            time.sleep(20)
            ll = f'https://mp.toutiao.com/video/video_system_thumb/?vid={upload_id}&item_id='
            thumb = requests.get(ll, headers=if_headers, verify=False).content.decode('utf-8')
            tb = json.loads(thumb)['data'][2]
            consss = '<p>{!-- PGC_VIDEO:{"sp":"toutiao","vid":"%s","vu":"%s","thumb_url":"%s","src_thumb_uri":"%s","vname":"%s"} --}</p>' % (
                upload_id, upload_id, tb['uri'], tb['src_uri'], name)
            uuu = 'https://mp.toutiao.com/core/article/edit_article_post/?source=mp&type=purevideo'
            title = name.replace('.mp4', '')
            if len(title) > 30:
                title = title[0:30]
            param = {'article_ad_type': '3', 'title': f'{title}', 'title_id': '1538976676585_1612724255524878',
                     'abstract': f'{name}',
                     'tag': 'video_funny', 'extern_link': '', 'is_fans_article': '0', 'content': consss,
                     'add_third_title': '0',
                     'timer_status': '0',
                     'timer_time': f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%m")}',
                     'recommend_auto_analyse': '0',
                     'govern_forward': '0', 'gov_forward_group_id': '-1', 'activity_tag': '0', 'column_selected': '',
                     'compass_video_id': '',
                     'compass_video_name': '', 'compass_video_type': '', 'article_label': '奇闻;恶搞;逗比;笑喷了',
                     'from_diagnosis': '0',
                     'article_type': '1', 'praise': '0', 'pgc_debut': '0', 'save': '1'}
            ddd = requests.post(uuu, data=param, headers=headers, verify=False).content.decode('utf-8')
            print(ddd)
        except Exception as e:
            print(e)


def uploadBr(tag,name, file):
    print(name)
    try:
        md5 = hashlib.md5()
        md5.update(file)
        md5 = md5.hexdigest()
        md5_check = f'https://mp.toutiao.com/video/video_uniq_api/?md5={md5}'
        md5_content = requests.get(md5_check, headers=md5_headers, verify=False).content.decode('utf-8')
        is_uniq = json.loads(md5_content)['is_uniq']
        if not is_uniq:
            return
        params = {'json_data': '{"api":"chunk_upload_info"}'}
        content = requests.post(url, data=params, headers=headers, verify=False).content.decode('utf-8')
        print(content)
        up_date = json.loads(json.loads(content)['data'])
        upload_id = up_date['upload_id']
        upload_url = up_date['upload_url'].replace('http', 'https')
        lens = len(file)
        requests.options(upload_url, headers=op_headers, verify=False)
        up_headers['Content-Range'] = f'bytes 0-{lens-1}/{lens}'
        multipart_encoder = MultipartEncoder(
            fields={
                'video_file': (name, file, 'application/octet-stream')
            },
            boundary='----WebKitFormBoundary' + str(random.randint(1e28, 1e29 - 1))
        )
        up_headers['Content-Type'] = multipart_encoder.content_type
        up_part = requests.post(upload_url, data=multipart_encoder, headers=up_headers, verify=False).content.decode(
            'utf-8')
        print(up_part)
        time.sleep(20)
        ll = f'https://mp.toutiao.com/video/video_system_thumb/?vid={upload_id}&item_id='
        thumb = requests.get(ll, headers=if_headers, verify=False).content.decode('utf-8')
        tb = json.loads(thumb)['data'][2]
        consss = '<p>{!-- PGC_VIDEO:{"sp":"toutiao","vid":"%s","vu":"%s","thumb_url":"%s","src_thumb_uri":"%s","vname":"%s"} --}</p>' % (
            upload_id, upload_id, tb['uri'], tb['src_uri'], name)
        uuu = 'https://mp.toutiao.com/core/article/edit_article_post/?source=mp&type=purevideo'
        title = name.replace('.mp4', '')
        if len(title) > 30:
            title = title[0:30]
        param = {'article_ad_type': '3', 'title': f'{title}', 'title_id': '1538976676585_1612724255524878',
                 'abstract': f'{name}',
                 'tag': tag, 'extern_link': '', 'is_fans_article': '0', 'content': consss,
                 'add_third_title': '0',
                 'timer_status': '0',
                 'timer_time': f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%m")}', 'recommend_auto_analyse': '0',
                 'govern_forward': '0', 'gov_forward_group_id': '-1', 'activity_tag': '0', 'column_selected': '',
                 'compass_video_id': '',
                 'compass_video_name': '', 'compass_video_type': '', 'article_label': '',
                 'from_diagnosis': '0',
                 'article_type': '1', 'praise': '0', 'pgc_debut': '0', 'save': '1'}
        ddd = requests.post(uuu, data=param, headers=headers, verify=False).content.decode('utf-8')
        print(ddd)
    except Exception as e:
        print(e)
