# -*- coding:utf-8 -*-
from pymongo import MongoClient
from model import DBSession, Tag
from datetime import datetime

__author__ = 'tangjiong'

r_db_counter = 0
w_db_counter = 0


def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

print '%s 开始统计过程' % current_time()
# 执行整个统计过程
for document in cursor:
    tags = document['tags']
    for q_tag in tags:
        r_db_counter += 1
        query = session.query(Tag).filter(Tag.tag_name == q_tag, Tag.date == date)
        if query.all():   # tag在数据库中
            tag_in_db = query.first()
            count = tag_in_db.tag_count  # 从数据库中取出的count，+1
            count += 1
            query.update({Tag.tag_count: count}, synchronize_session=False)
        else:
            # 不在数据库中，新建写入
            n_db_tag = Tag(tag_name=q_tag, tag_count=1, date=date)
            session.add(n_db_tag)
        w_db_counter += 1
        session.commit()

# 关闭数据库连接
session.close()
print '%s 统计完成' % current_time()
print '读数据库次数 %d' % r_db_counter
print '写数据库次数 %d' % w_db_counter