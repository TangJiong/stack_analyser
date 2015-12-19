# -*- coding:utf-8 -*-
__author__ = 'tangjiong'

BOT_NAME = 'stack_spider'

SPIDER_MODULES = ['stack_spider.spiders']
NEWSPIDER_MODULE = 'stack_spider.spiders'

ITEM_PIPELINES = ['stack_spider.pipelines.QuesItemPipleline', 'stack_spider.pipelines.TagItemPipleline']
MONGO_URI = "mongodb://localhost:27017/"    # 默认mongodb server地址
MONGO_DATABASE = "stack_db"