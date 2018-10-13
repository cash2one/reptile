#!/usr/bin/env python
# encoding: utf-8
#   @file: jrttnewsupload.py
#   @Created by shucheng.qu on 2018/10/13

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
    'Origin': 'https://mp.toutiao.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://mp.toutiao.com/profile_v3/graphic/publish',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'UM_distinctid=16618b95ff8fec-0fa240b9021b02-346a7809-13c680-16618b95ff962c; ccid=296a02fee1cb2bde36141ce9b5fb805b; tt_webid=6605715939382117896; _mp_test_key_1=8c5ba2f4856e1f876d04252a1c8384a1; odin_tt=262ede1235a3aeabad5bf1c22afdcce2e084b30e253823fdf3ceff9e01357cc2c7669544ca3074e1a37bc85418daaa04; toutiao_sso_user=c74691eabf1d099ea05c0454cf743e59; sso_login_status=1; login_flag=ba6e0a6676bb4d786cfdb690ba7205ba; sessionid=44d6b943ce601a25e0ce8e16c35bed71; sid_tt=44d6b943ce601a25e0ce8e16c35bed71; sso_uid_tt=d34e114a7e1528a0672cad21666554ce; uid_tt=e811dd21e8eb1b56ce7fd04963da74ea; sid_guard="44d6b943ce601a25e0ce8e16c35bed71|1538033885|15552000|Tue\054 26-Mar-2019 07:38:05 GMT"; uuid="w:de2c0423770643e5a4cc4a740d70f61e"; __tea_sdk__ssid=beec8374-ce22-4c85-85e8-0c0ec8728c41; _ga=GA1.2.690585305.1538033999; _ba=BA0.2-20180927-5110e-7cBJlpop5WtJMqHFzCGe; _mp_auth_key=d371927ba601cd61df6662a833cedb0d; tt_im_token=1538561362991433327555356191813192730245609901956983232219431908; __tea_sdk__user_unique_id=104777979000; _ga=GA1.3.690585305.1538033999; __utma=24953151.690585305.1538033999.1538793328.1538793328.1; __utmz=24953151.1538793328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gid=GA1.2.1813216214.1539399839; currentMediaId=1612724255524878; ptcn_no=839db58ef44ca0d2807dde791db58f40',
}

headers = {
    'Connection': 'keep-alive',
    'Origin': 'https://mp.toutiao.com',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://mp.toutiao.com/profile_v3/graphic/publish',
    'Cookie': 'UM_distinctid=16618b95ff8fec-0fa240b9021b02-346a7809-13c680-16618b95ff962c; ccid=296a02fee1cb2bde36141ce9b5fb805b; tt_webid=6605715939382117896; _mp_test_key_1=8c5ba2f4856e1f876d04252a1c8384a1; odin_tt=262ede1235a3aeabad5bf1c22afdcce2e084b30e253823fdf3ceff9e01357cc2c7669544ca3074e1a37bc85418daaa04; toutiao_sso_user=c74691eabf1d099ea05c0454cf743e59; sso_login_status=1; login_flag=ba6e0a6676bb4d786cfdb690ba7205ba; sessionid=44d6b943ce601a25e0ce8e16c35bed71; sid_tt=44d6b943ce601a25e0ce8e16c35bed71; sso_uid_tt=d34e114a7e1528a0672cad21666554ce; uid_tt=e811dd21e8eb1b56ce7fd04963da74ea; sid_guard="44d6b943ce601a25e0ce8e16c35bed71|1538033885|15552000|Tue\054 26-Mar-2019 07:38:05 GMT"; uuid="w:de2c0423770643e5a4cc4a740d70f61e"; __tea_sdk__ssid=beec8374-ce22-4c85-85e8-0c0ec8728c41; _ga=GA1.2.690585305.1538033999; _ba=BA0.2-20180927-5110e-7cBJlpop5WtJMqHFzCGe; _mp_auth_key=d371927ba601cd61df6662a833cedb0d; tt_im_token=1538561362991433327555356191813192730245609901956983232219431908; __tea_sdk__user_unique_id=104777979000; _ga=GA1.3.690585305.1538033999; __utma=24953151.690585305.1538033999.1538793328.1538793328.1; __utmz=24953151.1538793328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gid=GA1.2.781188670.1538911001; currentMediaId=1612724255524878; ptcn_no=6dbd2f538717f56aaa6e15126cb392e5'}

qr_headers = {
    'Connection': 'keep-alive',
    'Origin': 'https://mp.toutiao.com',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://mp.toutiao.com/profile_v3/graphic/publish',
    'Cookie': 'UM_distinctid=16618b95ff8fec-0fa240b9021b02-346a7809-13c680-16618b95ff962c; ccid=296a02fee1cb2bde36141ce9b5fb805b; tt_webid=6605715939382117896; _mp_test_key_1=8c5ba2f4856e1f876d04252a1c8384a1; odin_tt=262ede1235a3aeabad5bf1c22afdcce2e084b30e253823fdf3ceff9e01357cc2c7669544ca3074e1a37bc85418daaa04; toutiao_sso_user=c74691eabf1d099ea05c0454cf743e59; sso_login_status=1; login_flag=ba6e0a6676bb4d786cfdb690ba7205ba; sessionid=44d6b943ce601a25e0ce8e16c35bed71; sid_tt=44d6b943ce601a25e0ce8e16c35bed71; sso_uid_tt=d34e114a7e1528a0672cad21666554ce; uid_tt=e811dd21e8eb1b56ce7fd04963da74ea; sid_guard="44d6b943ce601a25e0ce8e16c35bed71|1538033885|15552000|Tue\054 26-Mar-2019 07:38:05 GMT"; uuid="w:de2c0423770643e5a4cc4a740d70f61e"; __tea_sdk__ssid=beec8374-ce22-4c85-85e8-0c0ec8728c41; _ga=GA1.2.690585305.1538033999; _ba=BA0.2-20180927-5110e-7cBJlpop5WtJMqHFzCGe; _mp_auth_key=d371927ba601cd61df6662a833cedb0d; tt_im_token=1538561362991433327555356191813192730245609901956983232219431908; __tea_sdk__user_unique_id=104777979000; _ga=GA1.3.690585305.1538033999; __utma=24953151.690585305.1538033999.1538793328.1538793328.1; __utmz=24953151.1538793328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gid=GA1.2.781188670.1538911001; currentMediaId=1612724255524878; ptcn_no=6dbd2f538717f56aaa6e15126cb392e5'}

o_headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.toutiao.com/profile_v3/graphic/publish',
    'Cookie': 'UM_distinctid=16618b95ff8fec-0fa240b9021b02-346a7809-13c680-16618b95ff962c; ccid=296a02fee1cb2bde36141ce9b5fb805b; tt_webid=6605715939382117896; _mp_test_key_1=8c5ba2f4856e1f876d04252a1c8384a1; odin_tt=262ede1235a3aeabad5bf1c22afdcce2e084b30e253823fdf3ceff9e01357cc2c7669544ca3074e1a37bc85418daaa04; toutiao_sso_user=c74691eabf1d099ea05c0454cf743e59; sso_login_status=1; login_flag=ba6e0a6676bb4d786cfdb690ba7205ba; sessionid=44d6b943ce601a25e0ce8e16c35bed71; sid_tt=44d6b943ce601a25e0ce8e16c35bed71; sso_uid_tt=d34e114a7e1528a0672cad21666554ce; uid_tt=e811dd21e8eb1b56ce7fd04963da74ea; sid_guard="44d6b943ce601a25e0ce8e16c35bed71|1538033885|15552000|Tue\054 26-Mar-2019 07:38:05 GMT"; uuid="w:de2c0423770643e5a4cc4a740d70f61e"; __tea_sdk__ssid=beec8374-ce22-4c85-85e8-0c0ec8728c41; _ga=GA1.2.690585305.1538033999; _ba=BA0.2-20180927-5110e-7cBJlpop5WtJMqHFzCGe; _mp_auth_key=d371927ba601cd61df6662a833cedb0d; tt_im_token=1538561362991433327555356191813192730245609901956983232219431908; __tea_sdk__user_unique_id=104777979000; _ga=GA1.3.690585305.1538033999; __utma=24953151.690585305.1538033999.1538793328.1538793328.1; __utmz=24953151.1538793328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gid=GA1.2.781188670.1538911001; currentMediaId=1612724255524878; ptcn_no=6dbd2f538717f56aaa6e15126cb392e5'}



img_upload = 'https://mp.toutiao.com/tools/upload_picture/?type=ueditor&pgc_watermark=1&action=uploadimage&encode=utf-8'

url = 'https://mp.toutiao.com/core/article/edit_article_post/?source=mp&type=article'

def _upload_img(src):
    try:
        file = requests.get(src, verify=False).content
        split = str(src).split('/')
        name = split[len(split) - 1]
        lens = len(file)
        img_headers['Content-Range'] = f'bytes 0-{lens-1}/{lens}'
        multipart_encoder = MultipartEncoder(
            fields={
                'type': 'image/png',
                'upfile': (name, file, 'application/octet-stream')
            },
            boundary='----WebKitFormBoundary' + str(random.randint(1e28, 1e29 - 1))
        )
        img_headers['Content-Type'] = multipart_encoder.content_type
        up_part = requests.post(img_upload, data=multipart_encoder, headers=img_headers,
                                verify=False).content.decode('utf-8')
        jsons = json.loads(up_part)
        # requests.post('https://mp.toutiao.com/article/check_qrcode/',data = {'image_urls':jsons['url']},headers=qr_headers,
        #                         verify=False).content.decode('utf-8')
        # upload_param = {'platform':'toutiaohao','position':'articleup_sub','image_info':'[{"url": "%s", "remark": "", "title": "","content": "", "width": %s, "height": %d}]'%(jsons["url"],jsons["width"],jsons["height"])}
        # requests.post('https://mp.toutiao.com/micro/image/upload',data = upload_param,headers=qr_headers,
        #                         verify=False).content.decode('utf-8')
        # uuu = F'https://mp.toutiao.com/micro/image/check?platform=toutiaohao&position=articleup_sub&image_url={jsons["url"]}&noCache={int(round(time.time() * 1000))}'
        # requests.get(uuu,headers=o_headers,verify=False).content.decode('utf-8')
        # time.sleep(1)
        # uuu = F'https://mp.toutiao.com/micro/image/check?platform=toutiaohao&position=articleup_sub&image_url={jsons["url"]}&noCache={int(round(time.time() * 1000))}'
        # requests.get(uuu,headers=o_headers,verify=False).content.decode('utf-8')
        return jsons
    except Exception as e:
        print(e)
        return None


def upload_news(path):
    with open(path) as file:
        title = ''
        introduction = ''
        content = []
        splits = str(file.read()).split('\n')
        for sp in splits:
            if sp.startswith('title'):
                title = sp.replace('title:','')
                continue
            if sp.startswith('introduction'):
                introduction = sp.replace('introduction:','')
                continue
            if sp.startswith('http'):
                jsons = _upload_img(sp)
                if jsons==None:
                    continue
                img = F'<div class="pgc-img"><img class="" src="{jsons["url"]}" data-ic="false" data-ic-uri="" data-height="{jsons["height"]}" data-width="{jsons["width"]}" image_type="{jsons["image_type"]}" web_uri="{jsons["wm_uri_media"]}" img_width="{jsons["width"]}" img_height="{jsons["height"]}"><p class="pgc-img-caption"></p></div>'
                content.append(img)
                continue
            content.append(F'<p>{sp}</p>')
        # requests.get('https://mp.toutiao.com/media/permissions/article/post/',headers=o_headers,verify=False).content.decode('utf-8')
        param = {
            'article_type': '0',
            'title': f'{title}',
            'content': ''.join(content),
            'activity_tag': '0',
            'title_id': '1539415376570_1612724255524878',
            'add_third_title': '0',
            'claim_origin': '0',
            'article_ad_type': '3',
            'recommend_auto_analyse': '0',
            'tag': '',
            'article_label': '',
            'is_fans_article': '0',
            'govern_forward': '0',
            'push_status': '0',
            'push_android_title': '',
            'push_android_summary': '',
            'push_ios_summary': '',
            'timer_status': '0',
            'timer_time': f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%m")}',
            'column_chosen': '0',
            'pgc_id': '0',
            'pgc_feed_covers': '[]',
            'need_pay': '0',
            'from_diagnosis': '0',
            'save': '1'}
        result = requests.post(url, data=param, headers=headers, verify=False).content.decode('utf-8')
        print(result)

if __name__ == "__main__":
    upload_news('/Users/macbook-HCI/pachong/news/1012/qtt/1111.txt')
