# stack_analyser
A python Project for course Business Intelligent aims to analyse the questions in stackoverflow, which includes two main parts, a spider based on scrpy and a web application based on flask. 

## Introduction
The project aims to find out what are the mostly asked questions every day and how they change with time in the famous Q&A site [stackoverflow][1]. Crawling all the questions is a quite simple job, as stackoverflow  has no anti-spider policy, so it's easy to get millions of questions with [scrapy][2]. However, it's not so easy to store so much data. As the data is in json format, so I choose [mongodb][3]. As for showing the analysis result, I use [flask][4] to build a simple web application, in which I make use of [highchats][5] to show the result in different graph and charts.

The following diagram shows structure of the whole project. 

## Screenshot
hottest topics
![screenshot][6]

how much share they account for
![screenshot][7]

how the change with time
![screenshot][8]

custom analysis
![screenshot][9]
![screenshot][10]
![screenshot][11]

search
![screenshot][12]
![screenshot][13]
![screenshot][14]

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
[6]:/screen_shot/index.png "the home page"
[7]:/screen_shot/topshares.png "the top shares page"
[8]:/screen_shot/toptrend.png "the top trend page"
[9]:/screen_shot/custom.png "the custom analysis page"
[10]:/screen_shot/custom_shares.png "the custom shares page"
[11]:/screen_shot/custom_trend.png "the custom trend page"
[12]:/screen_shot/custom_search.png "the custom search page"
[13]:/screen_shot/search_result.png "the search result page"
[14]:/screen_shot/single_tag.png "the single tag page"

