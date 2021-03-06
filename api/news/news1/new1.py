#!/usr/bin/env python
# encoding: utf-8
#   @file: new1.py
#   @Created by shucheng.qu on 2018/10/24
import json

# +------------------+---------------+------+-----+---------+----------------+
# | Field            | Type          | Null | Key | Default | Extra          |
# +------------------+---------------+------+-----+---------+----------------+
# | news_id          | int(11)       | NO   | PRI | NULL    | auto_increment |
# | news_title       | varchar(200)  | NO   | UNI | NULL    |                |
# | news_content     | mediumtext    | NO   |     | NULL    |                |
# | news_intro       | varchar(400)  | YES  |     | NULL    |                |
# | news_cover       | varchar(2000) | YES  |     | NULL    |                |
# | news_url         | varchar(300)  | YES  |     | NULL    |                |
# | news_type        | varchar(45)   | YES  |     | NULL    |                |
# | news_play        | int(11)       | YES  |     | NULL    |                |
# | news_comment     | int(11)       | YES  |     | NULL    |                |
# | news_comment_url | varchar(400)  | YES  |     | NULL    |                |
# | news_author      | varchar(45)   | YES  |     | NULL    |                |
# | news_author_img  | varchar(400)  | YES  |     | NULL    |                |
# | news_data        | varchar(45)   | YES  |     | NULL    |                |
# | news_source      | varchar(45)   | YES  |     | NULL    |                |
# | system_time      | bigint(20)    | YES  |     | NULL    |                |
# +------------------+---------------+------+-----+---------+----------------+
import time

from api.error import error1, error2
from db.dbbean import NewsBean
from db.mysql import getdb



def news1_result(q):
    if q == None or q == '':
        return error2
    db = getdb()
    try:
        loads = json.loads(q)
        size = 20
        day = 7
        if 'size' in loads:
            size = int(loads['size'])
            if size > 100:
                size = 100
        if 'day' in loads:
            day = int(loads['day'])
            if day > 10:
                day = 10
        mintime = day * 24 * 60 * 60 * 1000
        sql = 'SELECT news_id,news_title,news_cover,news_author FROM news WHERE RAND()<=0.01 and system_time > ((select max(system_time) from news) - %s) order by rand() limit %s ;'
        cursor = db.cursor()
        db.ping()
        cursor.execute(sql, ( mintime, size))
        fetchall = cursor.fetchall()
        data = []
        for item in fetchall:
            bean = {}
            bean['id'] = item[0]
            bean['title'] = item[1]
            temp = str(item[2])
            split = temp.split(';')
            img = []
            if len(split)>0:
                for ii in split:
                    if len(ii) >0:
                        img.append(ii)
            bean['cover'] = img
            bean['author'] = item[3]
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
