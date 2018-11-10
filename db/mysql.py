#!/usr/bin/env python
# encoding: utf-8
#   @file: mysql.py
#   @Created by shucheng.qu on 2018/10/20


# _*_encoding:UTF-8_*_
import pymysql

from db.dbbean import NewsBean, VideoBean

def getdb():
    return pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='quyuan9173', db='toutiao', charset='utf8')

def closedb(db):
    db.close()

def insert_news(bean: NewsBean,db):
    insertnews = "insert into news(news_title,news_content,news_intro,news_cover,news_url,news_type,news_play,news_comment,news_comment_url,news_author,news_author_img,news_data,news_source,system_time)"
    value = F" values ('{bean.news_title}','{bean.news_content}','{bean.news_intro}','{bean.news_cover}','{bean.news_url}','{bean.news_type}',{bean.news_play},{bean.news_comment},'{bean.news_comment_url}','{bean.news_author}','{bean.news_author_img}','{bean.news_data}','{bean.news_source}',{bean.system_time})"
    try:
        with db.cursor() as cursor:
            sql = insertnews + value
            cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

def insert_video(bean: VideoBean,db):
    insertvideo = "insert into video(video_title,video_url,video_intro,video_cover,video_play,video_type,video_comment,video_comment_url,video_author,video_author_img,video_data,video_source,video_md5,system_time)"
    value = F" values ('{bean.video_title}','{bean.video_url}','{bean.video_intro}','{bean.video_cover}',{bean.video_play},'{bean.video_type}',{bean.video_comment},'{bean.video_comment_url}','{bean.video_author}','{bean.video_author_img}','{bean.video_data}','{bean.video_source}','{bean.video_md5}',{bean.system_time})"
    try:
        with db.cursor() as cursor:
            sql = insertvideo + value
            cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

# sql20news = 'SELECT news_id,news_title,system_time FROM toutiao.news where system_time >= ((select max(system_time) from news) - (select min(system_time) from news))*rand() + (select min(system_time) from news) limit 10;'
# ttttttttt = 'SELECT * FROM toutiao.news where system_time >= ((select max(system_time) from news) - (select min(system_time) from news))*rand() + (select min(system_time) from news) limit 5;'

if __name__ == "__main__":
    # upload_news('/Users/macbook-HCI/pachong/news/1012/qtt/1111.txt')
    pass