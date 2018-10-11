#!/usr/bin/env python
# encoding: utf-8
#   @file: test.py
#   @Created by shucheng.qu on 2018/10/9
from newreptile.utils.test2 import sleeps

for index in range(0,20):
    print(index)
    sleeps(index)