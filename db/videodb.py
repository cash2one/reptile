#!/usr/bin/env python
# encoding: utf-8
#   @file: videodb.py
#   @Created by shucheng.qu on 2018/10/22
import random
import time

from db.dbbean import VideoBean
from db.mysql import getdb, closedb, insert_video


# +-------------------+
# | COLUMN_NAME       |
# +-------------------+
# | video_id          |
# | video_title        |
# | video_intro        |
# | video_type         |
# | video_comment      |
# | video_comment_url  |
# | video_author       |
# | video_author_img   |
# | video_data         |
# | video_url          |
# | video_play         |
# | video_cover        |
# | system_time       |
# | video_number      |
# +-------------------+

def save_db(db, title='', intro='', type='', cover='', url='', play=0, comment=0, comment_url='', author='',
            author_img='', data='', md5=''):
    time_flag = int(round(time.time() * 1000))
    time_flag = int(str(time_flag)[4:13])
    bean = VideoBean()
    bean.video_number = time_flag * 10 + random.randint(0, 9)
    bean.system_time = time_flag
    bean.video_title = title
    bean.video_intro = intro
    bean.video_cover = cover
    bean.video_url = url
    bean.video_play = play
    bean.video_comment = comment
    bean.video_comment_url = comment_url
    bean.video_type = type
    bean.video_author = author
    bean.video_author_img = author_img
    bean.video_data = data
    bean.video_md5 = md5
    insert_video(bean, db)


if __name__ == "__main__":
    # upload_news('/Users/macbook-HCI/pachong/news/1012/qtt/1111.txt')
    db = getdb()
    closedb(db)
    pass
