#!/usr/bin/env python
# encoding: utf-8
#   @file: video1.py
#   @Created by shucheng.qu on 2018/10/27
import json

from api.error import error2, error1
from db.mysql import getdb


def video1_result(q):
    if q == None or q == '':
        return error2
    db = getdb()
    try:
        loads = json.loads(q)
        size = 20
        day = 7
        if 'size' in loads.items():
            size = int(loads['size'])
            if size > 100:
                size = 100
        if 'day' in loads.items():
            day = int(loads['day'])
            if day > 10:
                day = 10
        mintime = day * 24 * 60 * 60 * 1000
        sql = 'SELECT video_id,video_title,video_url,video_cover,video_play,video_author,video_author_img FROM video WHERE RAND()<=0.5 and system_time > ((select max(system_time) from news) - %s) order by rand() limit %s ;'
        cursor = db.cursor()
        db.ping()
        cursor.execute(sql, ( mintime, size))
        fetchall = cursor.fetchall()
        data = []
        for item in fetchall:
            bean = {}
            bean['id'] = item[0]
            bean['title'] = item[1]
            bean['url'] = item[2]
            temp = str(item[3])
            split = temp.split(';')
            img = []
            if len(split)>0:
                for ii in split:
                    if len(ii) >0:
                        img.append(ii)
            bean['cover'] = img
            bean['play'] = item[4]
            bean['author'] = item[5]
            bean['author_img'] = item[6]
            data.append(bean)
        return json.dumps({'code': 0, 'data': data})
    except Exception as e:
        print(e)
        return error1
    finally:
        db.close()


if __name__ == '__main__':
    # news1_result('{"key":"234"}')
    pass