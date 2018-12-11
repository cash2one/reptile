#!/usr/bin/env python
# encoding: utf-8
#   @file: quanminxiaoshipin.py
#   @Created by shucheng.qu on 2018/11/29
import json
import os

import time

import emoji
import requests
from selenium import webdriver
import threading
import re
import hashlib

from newreptile.jinritoutiao.ascp import getASCP


# driver = webdriver.Chrome()
# driver.implicitly_wait(10)


def get(url, params=None, **kwargs):
    # , verify=False
    return requests.get(url, params=params, **kwargs)


def shell(shell):
    # 努比亚
    # shell = str(shell).replace('adb','adb -s 9e90f9ad')
    # 三星
    shell = str(shell).replace('adb','adb -s 947edaf4')
    print(shell)
    lines = ''
    for line in os.popen(shell):
        print(line)
        lines += '\n'
        lines += line
    return lines


def click(*args):
    shell(F'adb shell input tap {args[0]} {args[1]}')


def close(app):
    shell(F'adb shell am force-stop {app}')


def start(app):
    shell(F'adb shell am start -n {app}')


def input(msg):
    shell(F'adb shell am broadcast -a ADB_INPUT_TEXT --es msg {msg}')


def push():
    shell(F'adb push 111.mp4 /sdcard/DCIM/')


def refresh():
    shell('adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/DCIM/111.mp4')


def size():
    sizes = str(shell('adb shell wm size')).replace('Physical size: ', '').split('x')
    width = int(sizes[0])
    height = int(sizes[1])
    return width, height


def density():
    return int(str(shell('adb shell wm density')).replace('Physical density: ', '')) / 160


def douyin():
    header = {
        'Connection': 'keep-alive',
        'sdk-version': '1',
        'User-Agent': 'Aweme 3.4.0 rv:34008 (iPhone; iOS 12.1; zh_CN) Cronet',
        'X-SS-TC': '0',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': 'odin_tt=632f829d45776e089b261f6592b53d46d933a65654a9e6b685546008dc076bc6ae4ffde00540c9beac8bc623ba293a9f; install_id=52758939432; ttreq=1$b03dfe5f1a55e1ece4ee2cffa4678c2e949d5721'
    }

    vheader = {
        'Range': 'bytes=819200-',
        'Accept': '*/*',
        'User-Agent': 'Aweme/34008 CFNetwork/975.0.3 Darwin/18.2.0',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }

    url = 'https://aweme-eagle.snssdk.com/aweme/v1/feed/?version_code=3.4.0&pass-region=1&pass-route=1&js_sdk_version=1.3.0.1&app_name=aweme&vid=A7FCE49E-2B95-4CD8-88E2-06B1EFBC4D5E&app_version=3.4.0&device_id=57300219212&channel=App%20Store&aid=1128&screen_width=1242&openudid=34b191ae7037612aaea09c4055e59aaa0cdf85c5&os_api=18&ac=4G&os_version=12.1&device_platform=iphone&build_number=34008&iid=52758939432&device_type=iPhone9,2&idfa=557499F1-0018-41C0-83ED-DB523AF89315&volume=0.32&min_cursor=0&feed_style=0&filter_warn=0&count=6&pull_type=0&type=0&max_cursor=0&mas=011e277eecf2642dcfea13efe4121a40c82fe672c45f5427bee0c7&as=a1f53330c17c6cafe23374&ts=1543651265'
    list = get(url, headers=header).content.decode('utf-8')
    print(list)
    items = json.loads(list)['aweme_list']
    for item in items:
        title = item['desc'].replace('@', '').replace('抖音小助手', '').replace('/', '').replace('抖音', '').replace(' ', '').replace('#', '')
        title = emoji.get_emoji_regexp().sub('', title)
        videourl = item['video']['download_addr']['url_list'][0]
        videourl = str(videourl).replace(' ', '%20').replace('&watermark=1', '').replace('&logo_name=aweme','&version_code=3.4.0&pass-region=1&pass-route=1&js_sdk_version=1.3.0.1&app_name=aweme&vid=A7FCE49E-2B95-4CD8-88E2-06B1EFBC4D5E&app_version=3.4.0&device_id=57300219212&channel=App Store&aid=1128&screen_width=1242&openudid=34b191ae7037612aaea09c4055e59aaa0cdf85c5&os_api=18&ac=WIFI&os_version=12.1&device_platform=iphone&build_number=34008&iid=52758939432&device_type=iPhone9,2&idfa=557499F1-0018-41C0-83ED-DB523AF89315')
        href = get(videourl, headers=vheader).history[0].content.decode('utf-8')
        href = str(href).replace('<a href="', '').replace('">Found</a>.', '')
        print(title)
        print(href)
        with open(F'111.mp4', 'wb') as mp4:
            bmp4 = requests.get(href).content
            print(F'{title} {len(bmp4)}')
            if len(bmp4) < 500 or len(title) < 1 or item['is_ads']:
                continue
            mp4.write(bmp4)
            mp4.write(b'0x000x01')
        push()
        time.sleep(10)
        refresh()
        # upload_quduopai(title)
        upload_quanminxiaoshipin(title)
        time.sleep(60 * 1)
        # upload_huoshan(title)


def upload_quanminxiaoshipin(title):
    close('com.baidu.minivideo')
    time.sleep(5)
    start('com.baidu.minivideo/.app.activity.splash.SplashActivity')
    time.sleep(20)
    print('点击进入拍照')
    click(width * 0.5, height - 20 * dp)
    time.sleep(15)
    print('点击进入选择')
    click(0.5 * width + 115 * dp, height - 55 * dp)
    time.sleep(15)
    print('点击选择视频')
    click(width * 0.11296, height * 0.25677)
    time.sleep(40)
    print('点击进入编辑')
    click(width - dp * 45, height - 110 * dp)
    time.sleep(20)
    print('点击进入发布')
    click(width - 60 * dp, height - 54 * dp)
    time.sleep(30)
    input(title)
    time.sleep(50)
    print('点击发布')
    click(width - dp * 100, height - 55 * dp)
    time.sleep(15)
    close('com.baidu.minivideo')


def upload_quduopai(width, height, title):
    close('com.xike.yipai')
    time.sleep(5)
    start('com.xike.yipai/.view.activity.StartActivity')
    time.sleep(20)
    print('点击进入拍照')
    click(width * 0.5, height * 0.96875)
    time.sleep(10)
    print('点击进入选择')
    click(width * 0.22222, height * 0.91146)
    time.sleep(8)
    print('点击选择视频')
    shell(F'adb shell input tap {width*0.19907} {height*0.21354}')
    time.sleep(30)
    print('点击进入编辑')
    shell(F'adb shell input tap {width*0.84259} {height*0.96354}')
    time.sleep(10)
    print('点击进入输入')
    shell(F'adb shell input tap {width*0.18519} {height*0.79427}')
    time.sleep(5)
    print('输入')
    shell(F'adb shell am broadcast -a ADB_INPUT_TEXT --es msg {title}')
    time.sleep(5)
    print('点击确认输入')
    shell(F'adb shell input tap {width*0.87963} {height*0.92865}')
    time.sleep(5)
    print('点击发布')
    shell(F'adb shell input tap {width*0.70093} {height*0.95052}')
    time.sleep(30)
    shell('adb shell am force-stop com.xike.yipai')


def upload_huoshan(width, height, title):
    shell('adb shell am force-stop com.ss.android.ugc.live')
    time.sleep(5)
    shell('adb shell am start -n com.ss.android.ugc.live/.main.MainActivity')
    time.sleep(20)
    print('点击进入拍照')
    shell(F'adb shell input tap {width*0.5} {height*0.96354}')
    time.sleep(10)
    print('点击进入选择')
    shell(F'adb shell input tap {width*0.16203} {height*0.9651}')
    time.sleep(8)
    print('点击选择视频')
    shell(F'adb shell input tap {width*0.16203} {height*0.15625}')
    time.sleep(15)
    print('点击进入编辑')
    shell(F'adb shell input tap {width*0.87963} {height*0.03385}')
    time.sleep(30)
    print('点击进入输入')
    shell(F'adb shell input tap {width*0.75926} {height*0.91667}')
    time.sleep(10)
    print('点击输入')
    shell(F'adb shell input tap {width*0.68055} {height*0.23958}')
    time.sleep(5)
    print('输入')
    shell(F'adb shell am broadcast -a ADB_INPUT_TEXT --es msg {title}')
    time.sleep(5)
    print('点击发布')
    shell(F'adb shell input tap {width*0.5} {height*0.84115}')
    time.sleep(30)
    shell('adb shell am force-stop com.ss.android.ugc.live')


shell("adb shell ime set com.android.adbkeyboard/.AdbIME")
width, height = size()
dp = density()

for index in range(10):
    douyin()
shell('adb shell ime set com.sohu.inputmethod.sogou/.SogouIME')
