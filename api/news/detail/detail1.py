#!/usr/bin/env python
# encoding: utf-8
#   @file: detail1.py
#   @Created by shucheng.qu on 2018/10/30

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
import json

from api.error import error1, error2
from db.mysql import getdb


def detail1_result(q):
    if q == None or q == '':
        return error2
    db = getdb()
    try:
        loads = json.loads(q)
        if 'id' in loads:
            sql = 'SELECT news_title,news_content,news_author,news_author_img,news_data FROM news WHERE news_id = %s ;'
            cursor = db.cursor()
            db.ping()
            cursor.execute(sql, (loads['id']))
            fetch = cursor.fetchone()
            bean = {}
            bean['title'] = fetch[0]
            temp = str(fetch[1])
            split = temp.split('\n')
            content = []
            if len(split) > 0:
                for ii in split:
                    if len(ii) > 0:
                        content.append(ii)
            bean['content'] = content
            bean['author'] = fetch[2]
            bean['author_img'] = fetch[3]
            bean['data'] = fetch[4]
            return json.dumps({'code': 0, 'data': bean})
        else:
            return error2
    except Exception as e:
        print(e)
        return error1
    finally:
        db.close()

if __name__ == '__main__':
    # news1_result('{"key":"234"}')
    pass
