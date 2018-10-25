#!/usr/bin/env python
# encoding: utf-8
#   @file: dbbean.py
#   @Created by shucheng.qu on 2018/10/21

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

# type gaoxiao keji tiyu yule lishi junshi sannong meishi qiwen qiche xinlixue youxi redian
class NewsBean:
    news_title = ''
    news_content = ''
    news_intro = ''
    news_cover = ''
    news_url = ''
    news_type = ''
    news_play = 0
    news_comment = 0
    news_comment_url = ''
    news_author = ''
    news_author_img = ''
    news_data = ''
    news_source = ''
    system_time = 0


# +-------------------+---------------+------+-----+---------+----------------+
# | Field             | Type          | Null | Key | Default | Extra          |
# +-------------------+---------------+------+-----+---------+----------------+
# | video_id          | int(11)       | NO   | PRI | NULL    | auto_increment |
# | video_title       | varchar(200)  | NO   |     | NULL    |                |
# | video_url         | varchar(400)  | NO   |     | NULL    |                |
# | video_cover       | varchar(2000) | NO   |     | NULL    |                |
# | video_intro       | varchar(400)  | YES  |     | NULL    |                |
# | video_type        | varchar(45)   | YES  |     | NULL    |                |
# | video_play        | int(11)       | YES  |     | NULL    |                |
# | video_comment     | int(11)       | YES  |     | NULL    |                |
# | video_comment_url | varchar(300)  | YES  |     | NULL    |                |
# | video_author      | varchar(45)   | YES  |     | NULL    |                |
# | video_author_img  | varchar(300)  | YES  |     | NULL    |                |
# | video_data        | varchar(45)   | YES  |     | NULL    |                |
# | video_md5         | varchar(45)   | NO   | UNI | NULL    |                |
# | system_time       | bigint(20)    | YES  |     | NULL    |                |
# | video_source      | varchar(45)   | YES  |     | NULL    |                |
# +-------------------+---------------+------+-----+---------+----------------+
class VideoBean:
    video_title = ''
    video_url = ''
    video_cover = ''
    video_intro = ''
    video_type = ''
    video_play  = 0
    video_comment = 0
    video_comment_url = ''
    video_author = ''
    video_author_img = ''
    video_data = ''
    video_md5 = ''
    video_source = ''
    system_time = 0
