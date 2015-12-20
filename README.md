# stack_analyser
A python Project for course Business Intelligent aims to analyse the questions in stackoverflow, which includes two main parts, a spider based on scrpy and a web application based on flask. 

## Introduction
The project aims to find out what are the mostly asked questions every day and how they change with time in the famous Q&A site [stackoverflow][1]. Crawling all the questions is a quite simple job, as stackoverflow  has no anti-spider policy, so it's easy to get millions of questions with [scrapy][2]. However, it's not so easy to store so much data. As the data is in json format, so I choose [mongodb][3]. As for showing the analysis result, I use [flask][4] to build a simple web application, in which I make use of [highchats][5] to show the result in different graph and charts.

The following diagram shows structure of the whole project. 

## Setup
1. clone the project.
2. install mongodb(skip if exists) and create database stack_db in mongodb.
3. install mysql(skip if exists), create database stack_db, create table tag(id, tagname, tag_count, date) in stack_db.
4. open the project with PyCharm, both stack_analyser and stack_spider.
5. run the stack_spider to crawl questions from stackoverflow.
6. run static_cache.py in stack_analyser to do some statistis and data transfer.
7. run the stack_analyser for final result.

[1]:http://stackoverflow.com "stckoverflow"
[2]:http://scrapy.org/ "scrapy"
[3]:https://www.mongodb.org/ "mongodb"
[4]:https://dormousehole.readthedocs.org/en/latest/ "flask"
[5]:http://www.highcharts.com/ "highcharts"

