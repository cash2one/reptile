#!/usr/bin/env python
# encoding: utf-8
#   @file: ucnews.py
#   @Created by shucheng.qu on 2018/10/23
import requests

cc = requests.get('http://m.uczzd.cn/ucnews/news?app=ucnews-iflow&aid=6411126660293854762&cid=100&zzd_from=ucnews-iflow&uc_param_str=dndsfrvesvntnwpfgibi&recoid=4664998969846007145&rd_type=reco&activity=1&activity2=1').content.decode('utf-8')
print(cc)