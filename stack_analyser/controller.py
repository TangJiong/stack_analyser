# -*- coding:utf-8 -*-
from flask import json
from model import DBSession, Tag, engine, mongo_stack_db
from datetime import datetime, date, timedelta
from calendar import monthrange
import pymongo

__author__ = 'tangjiong'

session = DBSession()


def get_toprank(period="day", top=10):
    # 事实上，这里查询到的都是前一天的数据，当天的数据
    # 要在这一天结束时才能统计
    # 当天日期
    current_date = date.today()
    if period == "day":
        # TODO
        query_date = current_date - timedelta(days=1)
        # TODO
        # sql: select * from tag where date = '2014-03-01' order by tag_count desc limit 10
        result = session.query(Tag).filter(Tag.date == "2014-03-01").order_by(Tag.tag_count.desc()).limit(top).all()
        taglist = []
        for tag in result:
            taglist.append({
                "tag_name": tag.tag_name,
                "tag_count": tag.tag_count,
            })
        data = {
            "date": query_date.isoformat(),
            "taglist": taglist
        }
        return json.dumps(data)
    elif period == "week":
        # sql: select tag_name, sum(tag_count) as count from tag where date between
        #  '2014-02-24' and '2014-03-01' group by tag_name order by count desc limit 20
        # TODO
        end_date = current_date - timedelta(days=1)
        gap_days = date.isoweekday(end_date)
        start_date = end_date - timedelta(days=gap_days)
        # TODO
        sql = "select tag_name,sum(tag_count) as count from tag "
        sql += "where date between '2014-02-27' and '2014-03-01' "
        sql += "group by tag_name order by count desc limit " + str(top)
        result = engine.execute(sql)
        taglist = []
        for tag in result.fetchall():
            taglist.append({
                "tag_name": str(tag["tag_name"]),
                "tag_count": int(tag["count"]),
            })
        data = {
            "date": start_date.isoformat() + " - " + end_date.isoformat(),
            "taglist": taglist
        }
        return json.dumps(data)
    elif period == "month":
        # sql: select tag_name, sum(tag_count) as count from tag where date between
        #  '2014-02-24' and '2014-03-01' group by tag_name order by count desc limit 20
        # TODO
        end_date = current_date - timedelta(days=1)
        gap_days = end_date.day - 1
        start_date = end_date - timedelta(days=gap_days)
        # TODO
        sql = "select tag_name,sum(tag_count) as count from tag "
        sql += "where date between '2014-02-27' and '2014-03-01' "
        sql += "group by tag_name order by count desc limit " + str(top)
        result = engine.execute(sql)
        taglist = []
        for tag in result.fetchall():
            taglist.append({
                "tag_name": str(tag["tag_name"]),
                "tag_count": int(tag["count"]),
            })
        data = {
            "date": start_date.isoformat() + " - " + end_date.isoformat(),
            "taglist": taglist
        }
        return json.dumps(data)
    elif period == "year":
        # sql: select tag_name, sum(tag_count) as count from tag where date between
        #  '2014-02-24' and '2014-03-01' group by tag_name order by count desc limit 20
        # TODO
        end_date = current_date - timedelta(days=1)
        start_date = str(end_date.year) + "-01-01"
        # TODO
        sql = "select tag_name,sum(tag_count) as count from tag "
        sql += "where date between '2014-02-27' and '2014-03-01' "
        sql += "group by tag_name order by count desc limit " + str(top)
        result = engine.execute(sql)
        taglist = []
        for tag in result.fetchall():
            taglist.append({
                "tag_name": str(tag["tag_name"]),
                "tag_count": int(tag["count"]),
            })
        data = {
            "date": start_date + " to " + end_date.isoformat(),
            "taglist": taglist
        }
        return json.dumps(data)
    elif period == "total":
        # sql: select tag_name, sum(tag_count) as count from tag
        # group by tag_name order by count desc limit 20
        sql = "select tag_name,sum(tag_count) as count from tag "
        sql += "group by tag_name order by count desc limit " + str(top)
        result = engine.execute(sql)
        taglist = []
        for tag in result.fetchall():
            taglist.append({
                "tag_name": str(tag["tag_name"]),
                "tag_count": int(tag["count"]),
            })
        data = {
            "date": "from very beginning to now",
            "taglist": taglist
        }
        return json.dumps(data)


def get_topshares(period, top):
    return get_toprank(period, top)


def get_toptrend(recent, period, top):
    # 事实上，这里查询到的都是前一天的数据，当天的数据
    # 要在这一天结束时才能统计
    # 当天日期
    # current_date = date(2014, 3, 5)
    if period == "day":
        # TODO
        current_date = date(2014, 3, 5)
        end_date = current_date - timedelta(days=1)
        start_date = end_date - timedelta(days=int(recent))
        datelist = []
        for x in range(int(recent)):
            datelist.append(current_date.isoformat())
            current_date = current_date - timedelta(days=1)
        datelist.reverse()
        # TODO
        # sql: select * from tag where date = '2014-03-01' order by tag_count desc limit 10
        # 先找出当天的top，然后再查询top里的每一条数据
        result = session.query(Tag).filter(Tag.date == "2014-03-01").order_by(Tag.tag_count.desc()).limit(top).all()
        taglist = []
        for tag in result:
            # 每个top在指定时间段内的数据
            sql = "select * from tag "
            sql += "where tag_name = '" + tag.tag_name + "' and date between '2014-02-24' and '2014-03-04'"
            sql += "order by date asc"
            tag_records = engine.execute(sql)
            count_array = []
            for tag_record in tag_records.fetchall():
                count_array.append(int(tag_record['tag_count']))
            taglist.append({
                "tag_name": tag.tag_name,
                "count_array": count_array
            })
        data = {
            "date": start_date.isoformat() + " - " + end_date.isoformat(),
            "taglist": taglist,
            "datelist": datelist
        }
        return json.dumps(data)
    elif period == "month":
        current_date = date(2014, 7, 1)
        datelist = []
        for x in range(int(recent)):
            datelist.append(current_date.isoformat()[0:7])
            current_date = current_date - timedelta(days=monthrange(current_date.year, current_date.month)[1])
        # datelist.reverse()
        # sql: select * from tag where date = '2014-03-01' order by tag_count desc limit 10
        # 先找出当天的top，然后再查询top里的每一条数据
        result = session.query(Tag).filter(Tag.date == "2014-03-01").order_by(Tag.tag_count.desc()).limit(top).all()
        taglist = []
        for tag in result:
            count_array = []
            for query_date in datelist:
                sql = "select tag_name, sum(tag_count) as count from tag "
                sql += "where tag_name = '" + tag.tag_name + "' and date like '%" + query_date + "%'"
                tag_record = engine.execute(sql).fetchone()
                count_array.append(tag_record['count'])
            # count_array.reverse()
            taglist.append({
                "tag_name": tag.tag_name,
                "count_array": count_array
            })
        data = {
            "date": datelist[0] + " - " + datelist[int(recent)-1],
            "taglist": taglist,
            "datelist": datelist
        }
        return json.dumps(data)
    elif period == "year":
        current_date = date(2015, 12, 9)
        datelist = []
        for x in range(int(recent)):
            datelist.append(current_date.year)
            current_date = date(current_date.year-1, current_date.month, current_date.day)
        # sql: select * from tag where date = '2014-03-01' order by tag_count desc limit 10
        # 先找出当天的top，然后再查询top里的每一条数据
        result = session.query(Tag).filter(Tag.date == "2014-03-01").order_by(Tag.tag_count.desc()).limit(top).all()
        taglist = []
        for tag in result:
            count_array = []
            for query_date in datelist:
                sql = "select tag_name, sum(tag_count) as count from tag "
                sql += "where tag_name = '" + tag.tag_name + "' and date like '%" + str(query_date) + "%'"
                tag_record = engine.execute(sql).fetchone()
                count_array.append(tag_record['count'])
            # count_array.reverse()
            taglist.append({
                "tag_name": tag.tag_name,
                "count_array": count_array
            })
        data = {
            "date": str(datelist[0]) + " - " + str(datelist[int(recent)-1]),
            "taglist": taglist,
            "datelist": datelist
        }
        return json.dumps(data)


def search_tag(keyword):
    cursor = mongo_stack_db.tags.find(
        {"tagname": {"$regex": keyword + ".*"}},  # 查询条件
        {"_id": 0}
    ).limit(10)
    taglist = []
    for document in cursor:
        taglist.append(document)
    return json.dumps(taglist)


def get_top_tags(size):
    cursor = mongo_stack_db.tags.find({}, {"_id": 0})\
        .sort("questotal", pymongo.DESCENDING).limit(size)
    taglist = []
    for document in cursor:
        taglist.append(document)
    return json.dumps(taglist)


def get_tag_info(tagname, recent):
    # 事实上，这里查询到的都是前一天的数据，当天的数据
    # 要在这一天结束时才能统计
    # 当天日期
    # current_date = date(2014, 3, 5)
    # TODO
    current_date = date(2014, 3, 5)
    end_date = current_date - timedelta(days=1)
    start_date = end_date - timedelta(days=int(recent))
    datelist = []
    for x in range(int(recent)):
        datelist.append(current_date.isoformat())
        current_date = current_date - timedelta(days=1)
    datelist.reverse()
    # TODO
    # tag在指定时间段内的数据
    sql = "select * from tag "
    sql += "where tag_name = '" + tagname + "' and date between '2014-02-24' and '2014-03-04'"
    sql += "order by date asc"
    tag_records = engine.execute(sql)
    count_array = []
    for tag_record in tag_records.fetchall():
        count_array.append(int(tag_record['tag_count']))
    data = {
        "date": start_date.isoformat() + " - " + end_date.isoformat(),
        "tagname": tagname,
        "count_array": count_array,
        "datelist": datelist
    }
    return json.dumps(data)


def get_custom_shares(_taglist, start_date, end_date):
    taglist = []
    for tagname in _taglist:
        # sql: select tag_name, sum(tag_count) as count from tag
        # where tag_name = 'tagname' and date between '2014-02-24' and '2014-03-01'
        sql = "select tag_name,sum(tag_count) as count from tag "
        sql += "where tag_name = '" + tagname + "' and date between '" + start_date + "' and '" + end_date + "' "
        result = engine.execute(sql)
        tag = result.fetchone()
        taglist.append({
            "tag_name": str(tag["tag_name"]),
            "tag_count": int(tag["count"]),
        })
    data = {
        "date": start_date + " - " + end_date,
        "taglist": taglist
    }
    return json.dumps(data)


def get_custom_trend(_taglist, _start_date, _end_date):
    taglist = []
    for tag_name in _taglist:
        # 每个tag在指定时间段内的数据
        sql = "select * from tag "
        sql += "where tag_name = '" + tag_name + "' and date between '" + _start_date + "' and '" + _end_date + "'"
        sql += "order by date asc"
        tag_records = engine.execute(sql)
        count_array = []
        for tag_record in tag_records.fetchall():
            count_array.append(int(tag_record['tag_count']))
        taglist.append({
            "tag_name": tag_name,
            "count_array": count_array
        })
    end_date = datetime.strptime(_end_date, '%Y-%m-%d').date()
    start_date = datetime.strptime(_start_date, '%Y-%m-%d').date()
    datelist = []
    datelist.append(end_date.isoformat())
    while cmp(start_date.isoformat(), end_date.isoformat()) != 0:
        end_date = end_date - timedelta(days=1)
        datelist.append(end_date.isoformat())

    datelist.reverse()
    data = {
        "date": _start_date + " - " + _end_date,
        "taglist": taglist,
        "datelist": datelist
    }
    return json.dumps(data)
