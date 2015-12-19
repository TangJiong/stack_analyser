# -*- coding:utf-8 -*-

__author__ = 'tangjiong'
import pymongo


class QuesItemPipleline(object):
    """
    处理数据，在这里是把数据存入MongoDB
    """

    collection_name = 'questions'

    def __init__(self, mongo_uri, mongo_db):
        """
        初始化方法，初始化数据库连接
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'stack_ques_spider':
            self.db[self.collection_name].insert(dict(item))
            return item
        return item


class TagItemPipleline(object):
    """
    处理数据，在这里是把数据存入MongoDB
    """

    collection_name = 'tags'

    def __init__(self, mongo_uri, mongo_db):
        """
        初始化方法，初始化数据库连接
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'stack_tags_spider':
            self.db[self.collection_name].insert(dict(item))
            return item
        return item
