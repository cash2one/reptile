#!/usr/bin/env python
# encoding: utf-8
#   @file: test.py
#   @Created by shucheng.qu on 2018/12/3
import hashlib

import requests

url = 'http://v3-dy.ixigua.com/de1dd4b36ae55019736acc1256bb2ed2/5c04a050/video/m/220a1e6ed2ff7604294a3df15fe6e309ee811610aa4e000058c6c3c6b5fa/?rc=ajxpczR0NmVvajMzZGkzM0ApQHRAbzVFPDw0NzQzNDk6MzY1OzNAKXUpQGczdylAZmxkamV6aGhkZjs0QGlmZzAuMWFwLl8tLS4tL3NzLW8jbyMvNi8zNC0uLS0vLi4tLi4vaTpiLW8jOmAtbyNtbCtiK2p0OiMvLl4%3D'

bmp4 = requests.get(url).content

md5 = hashlib.md5()
md5.update(bmp4)
md5 = md5.hexdigest()
print(md5)

with open(F'1111.mp4', 'wb') as mp41:
    mp41.write(bmp4)
    mp41.write(b'0x000x01')
with open(F'111.mp4', 'rb') as mp41:
    md5 = hashlib.md5()
    md5.update(mp41.read())
    md5 = md5.hexdigest()
    print(md5)
