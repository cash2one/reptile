#!/usr/bin/env python
# encoding: utf-8
#   @file: video_request.py
#   @Created by shucheng.qu on 2018/10/27
import json

from api.error import error1
from api.video.video1.video1 import video1_result


def video(q,key):
    try:
        data = json.loads(q)
        version = data['version']
        if version ==1:
            return video1_result(q)
        elif version ==2:
            pass
        else:
            pass
    except Exception:

        return error1


if __name__ == '__main__':
    pass