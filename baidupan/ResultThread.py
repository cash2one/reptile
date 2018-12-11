#!/usr/bin/env python
# encoding: utf-8
#   @file: ResultThread.py
#   @Created by shucheng.qu on 2018/11/19

from threading import Thread

import time


class ResultThread(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target:
            self._return = self._target(self._args)

    def join(self, timeout=None):
        Thread.join(self, timeout)
        return self._return
