# -*- coding:utf-8 -*-
from pymongo import MongoClient
from model import DBSession, Tag
from datetime import datetime

__author__ = 'tangjiong'

cache_hit = 0
r_db_counter = 0
w_db_counter = 0

tag_cache = [
    {'name': 'javascript', 'count': 0},
    {'name': 'java', 'count': 0},
    {'name': 'c#', 'count': 0},
    {'name': 'php', 'count': 0},
    {'name': 'android', 'count': 0},
    {'name': 'jquery', 'count': 0},
    {'name': 'python', 'count': 0},
    {'name': 'html', 'count': 0},
    {'name': 'c++', 'count': 0},
    {'name': 'ios', 'count': 0},
    {'name': 'mysql', 'count': 0},
    {'name': 'css', 'count': 0},
    {'name': 'sql', 'count': 0},
    {'name': 'asp.net', 'count': 0},
    {'name': 'objective-c', 'count': 0}
]


def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_tag_from_cache(tag_name):
    """ 尝试从cache中获取标签
    :param tag_name:
    :return: 存在返回tag，不在返回None
    """
    for tag in tag_cache:
        if tag['name'] == tag_name:
            global cache_hit
            cache_hit += 1
            return tag
    return None


def write_tag_to_db(tag):
    """ 将标签数据写入数据库，数据库已有记录，更新；没有，新增
    :param tag:
    :return:
    """
    local_query = session.query(Tag).filter(Tag.tag_name == tag['name'], Tag.date == date)
    global r_db_counter
    r_db_counter += 1
    if local_query.all():   # 数据库中有记录
        local_query.update({Tag.tag_count: tag['count']}, synchronize_session=False)
    else:   # 数据库中没有记录
        new_db_tag = Tag(tag_name=tag['name'], tag_count=tag['count'], date=date)
        session.add(new_db_tag)
    global w_db_counter
    w_db_counter += 1
    session.commit()


def pop_cache_tag():
    """ 将缓存中的数据写入db
    """
    for tag in tag_cache:
        write_tag_to_db(tag)


# ======================================================================
print '%s 程序启动' % current_time()

client = MongoClient()
db = client.stack_db
date = '2014-07-01'
# 查询每一天的问题，貌似很慢，估计检索整个库吧，数据量太大真是可怕
cursor = db.questions.find(
    {"timestamp": {"$regex": date + ".*"}},   # 查询条件
    {"_id": 0, "title": 1, "timestamp": 1, "tags": 1}    # projection
)

print '%s 完成mongo查询' % current_time()

#  创建mysql连接session
session = DBSession()

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
            query = session.query(Tag).filter(Tag.tag_name == q_tag, Tag.date == date)
            r_db_counter += 1
            if query.all():   # tag在数据库中
                tag_in_db = query.first()
                count = tag_in_db.tag_count  # 从数据库中取出的count，+1
                count += 1
                query.update({Tag.tag_count: count}, synchronize_session=False)
            else:
                # 不在数据库中，新建写入
                n_db_tag = Tag(tag_name=q_tag, tag_count=1, date=date)
                session.add(n_db_tag)
            session.commit()
            w_db_counter += 1

# 清空cache
pop_cache_tag()
session.close()
print '%s 统计完成' % current_time()
print 'cache命中 %d' % cache_hit
print '读数据库次数 %d' % r_db_counter
print '写数据库次数 %d' % w_db_counter