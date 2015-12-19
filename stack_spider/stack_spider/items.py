# -*- coding:utf-8 -*-

__author__ = 'tangjiong'

import scrapy


class QuesItem(scrapy.Item):
    """ 问题的数据结构 """
    title = scrapy.Field()  # 标题
    summary = scrapy.Field()  # 摘要
    tags = scrapy.Field()  # 标签
    timestamp = scrapy.Field()  # 时间戳
    vote_count = scrapy.Field()  # 投票数
    answer_count = scrapy.Field()  # 回答数
    view_count = scrapy.Field()  # 浏览数


class TagItem(scrapy.Item):
    """ 标签的数据结构 """
    tagname = scrapy.Field()
    taglink = scrapy.Field()
    questotal = scrapy.Field()
    # todayasked = scrapy.Field()
    # weekasked = scrapy.Field()

