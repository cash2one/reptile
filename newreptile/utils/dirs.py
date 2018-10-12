#!/usr/bin/env python
# encoding: utf-8
#   @file: dirs.py
#   @Created by shucheng.qu on 2018/10/1

import os
import datetime


def makedirs(path,*paths):
    temp = ''
    for pa in paths:
        temp+='/'
        temp+=pa
    path = F'{os.environ["HOME"]}/pachong/{path}/{datetime.datetime.now().strftime("%m%d")}/{temp}'
    if os.path.exists(path) == False:
        os.makedirs(path)
    return path