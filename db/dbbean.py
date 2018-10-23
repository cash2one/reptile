#!/usr/bin/env python
# encoding: utf-8
#   @file: dbbean.py
#   @Created by shucheng.qu on 2018/10/21

# +------------------+
# | COLUMN_NAME      |
# +------------------+
# | news_id          |
# | news_title       |
# | news_intro       |
# | news_content     |
# | news_url         |
# | news_comment     |
# | news_comment_url |
# | news_type        |
# | news_author      |
# | news_author_img  |
# | news_data        |
# | system_time      |
# | news_cover       |
# | news_number      |
# | news_play        |
# +------------------+

# type gaoxiao keji tiyu yule lishi junshi sannong meishi qiwen qiche xinlixue youxi redian
class NewsBean:
    news_number = 0
    news_title = ''
    news_intro = ''
    news_content = ''
    news_cover = ''
    news_url = ''
    news_play = 0
    news_comment = 0
    news_comment_url = ''
    news_type = ''
    news_author = ''
    news_author_img = ''
    news_data = ''
    system_time = 0


# +-------------------+
# | COLUMN_NAME       |
# +-------------------+
# | video_id          |
# | video_title       |
# | video_intro       |
# | video_type        |
# | video_comment     |
# | video_comment_url |
# | video_author      |
# | video_author_img  |
# | video_data        |
# | video_url         |
# | video_play        |
# | video_cover       |
# | system_time       |
# | video_number      |
# +-------------------+

class VideoBean:
    video_number = 0
    video_title = ''
    video_intro = ''
    video_url = ''
    video_cover = ''
    video_play  = 0
    video_type = ''
    video_comment = 0
    video_comment_url = ''
    video_author = ''
    video_author_img = ''
    video_data = ''
    system_time = 0
    video_md5 = ''
