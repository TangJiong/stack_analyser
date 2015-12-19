# -*- coding:utf-8 -*-
from pymongo import MongoClient
from collections import deque
from model import DBSession, Tag
from datetime import datetime

__author__ = 'tangjiong'

cache_hit = 0
r_db_counter = 0
w_db_counter = 0


def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_tag_from_cache(tag_name):
    """ 尝试从cache中获取标签
    :param tag_name:
    :return: 存在返回tag，不在返回None
    """
    for tag in tag_cache_queue:
        if tag['name'] == tag_name:
            global cache_hit
            cache_hit += 1
            return tag
    return None


def get_tag_from_db(tag_name):
    """ 尝试从数据库中获取标签
    :param tag_name:
    :return: 存在返回tag，不在返回None
    """
    query = session.query(Tag).filter(Tag.tag_name == tag_name, Tag.date == date)
    global r_db_counter
    r_db_counter += 1
    if query.all():
        # 从数据库里查询标签
        tag_in_db = query.first()
        tag = {'name': tag_name, 'count': tag_in_db.tag_count}
        return tag
    return None


def write_tag_to_db(tag):
    """ 将标签数据写入数据库，数据库已有记录，更新；没有，新增
    :param tag:
    :return:
    """
    query = session.query(Tag).filter(Tag.tag_name == tag['name'], Tag.date == date)
    global r_db_counter
    r_db_counter += 1
    if query.all():   # 数据库中有记录
        query.update({Tag.tag_count: tag['count']}, synchronize_session=False)
    else:   # 数据库中没有记录
        n_db_tag = Tag(tag_name=tag['name'], tag_count=tag['count'], date=date)
        session.add(n_db_tag)
    global w_db_counter
    w_db_counter += 1
    session.commit()


def safe_cache_tag(tag):
    """ 用安全的方式将tag存入cache
    如果cache没满，直接append到尾部
    如果满了，pop掉头部的tag，写入数据库，再append到尾部
    :param tag:
    :return:
    """
    if len(tag_cache_queue) < CACHE_SIZE:
        tag_cache_queue.append(tag)
    else:
        # c_h_tag means cached_header_tag
        c_h_tag = tag_cache_queue.popleft()
        write_tag_to_db(c_h_tag)
        tag_cache_queue.append(tag)


def safe_clear_cache():
    """ 安全清空cache，其实就是将cache中的数据写入数据库
    :return:
    """
    for tag in tag_cache_queue:
        write_tag_to_db(tag)
    tag_cache_queue.clear()

# ======================================================================
print '%s 程序启动' % current_time()

client = MongoClient()
db = client.stack_db
date = '2014-03-01'
# 查询每一天的问题，貌似很慢，估计检索整个库吧，数据量太大真是可怕
cursor = db.questions.find(
    {"timestamp": {"$regex": date + ".*"}},   # 查询条件
    {"_id": 0, "title": 1, "timestamp": 1, "tags": 1}    # projection
)

print '%s 完成mongo查询' % current_time()

#  创建mysql连接session
session = DBSession()

# 创建一个cache_queue，用于缓存标签统计数据，减少数据库读写次数
CACHE_SIZE = 20
tag_cache_queue = deque()

print '%s 开始统计过程' % current_time()

# 执行整个统计过程
for document in cursor:
    tags = document['tags']
    for q_tag in tags:
        # 尝试从cache中取出标签
        c_tag = get_tag_from_cache(q_tag)
        if c_tag:
            # 不空表示在cache中，取出tag，count++
            # 这个能不能修改cache里面的值啊，不知道c_tag返回的是副本还是引用
            c_tag['count'] += 1
        else:
            # 不在缓存中，尝试从数据库中取出
            db_tag = get_tag_from_db(q_tag)
            if db_tag:
                # 不空，在数据库中，取出记录，count++，存入cache
                name = db_tag['name']  # 从数据库中取出的name
                count = db_tag['count']  # 从数据库中取出的count
                count += 1
                # n_c_tag means new_cache_tag
                n_c_tag = {'name': name, 'count': count}
                safe_cache_tag(n_c_tag)
            else:
                # 不在数据库中，存入cache，等待被写入db
                # n_c_tag means new_cache_tag
                n_c_tag = {'name': q_tag, 'count': 1}
                safe_cache_tag(n_c_tag)
# 清空cache
safe_clear_cache()
session.close()
print '%s 统计完成' % current_time()
print 'cache命中 %d' % cache_hit
print '读数据库次数 %d' % r_db_counter
print '写数据库次数 %d' % w_db_counter