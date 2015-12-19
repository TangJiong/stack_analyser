# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, create_engine, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient

__author__ = 'tangjiong'

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/stack_db')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 创建对象基类
Base = declarative_base()

# mongodb连接
mongo_client = MongoClient()
mongo_stack_db = mongo_client.stack_db


# 定义对象
class Tag(Base):

    __tablename__ ='tag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String(30))
    tag_count = Column(Integer, default=0)
    date = Column(Date)


