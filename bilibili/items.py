# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class UploaderItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    face_url = scrapy.Field()
    auth_description = scrapy.Field()
    following_number = scrapy.Field()
    follower_number = scrapy.Field()

class FollowItem(scrapy.Item):
    # 发起关注id
    following_id = scrapy.Field()
    # 被关注者id
    follower_id = scrapy.Field()

class FollowListItem(scrapy.Item):
    follow_list = scrapy.Field()

