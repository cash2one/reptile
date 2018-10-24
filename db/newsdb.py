#!/usr/bin/env python
# encoding: utf-8
#   @file: newsdb.py
#   @Created by shucheng.qu on 2018/10/21


# class NewsBean:
#     news_number = 0
#     news_title = ''
#     news_intro = ''
#     news_content = ''
#     news_cover = ''
#     news_play = 0
#     news_comment = 0
#     news_comment_url = ''
#     news_type = ''
#     news_author = ''
#     news_author_img = ''
#     news_data = ''
#     system_time = 0
import random
import time

from db.dbbean import NewsBean
from db.mysql import insert_news, getdb, closedb


def save_db(db, title='', intro='', content='', cover='', url='', play=0, comment=0, comment_url='', type='', author='',
            author_img='', data=''):
    time_flag = int(round(time.time() * 1000))
    bean = NewsBean()
    bean.system_time = time_flag
    bean.news_number = time_flag * 100 + random.randint(10, 99)
    bean.news_title = title
    bean.news_intro = intro
    bean.news_content = content
    bean.news_cover = cover
    bean.news_url = url
    bean.news_play = play
    bean.news_comment = comment
    bean.news_comment_url = comment_url
    bean.news_type = type
    bean.news_author = author
    bean.news_author_img = author_img
    bean.news_data = data
    insert_news(bean, db)


if __name__ == "__main__":
    # upload_news('/Users/macbook-HCI/pachong/news/1012/qtt/1111.txt')
    db = getdb()
    save_db(db, title='ddd', intro='ddsdsd', content='ffdsfsd', cover='sfdfds', url='dsjfnjdf', play=12, comment=23,
            comment_url='eeffewf', type='wewe', author='wqre', author_img='qweuhwue', data='wewqe')
    closedb(db)
    pass
