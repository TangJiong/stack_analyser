# -*- coding:utf-8 -*-

__author__ = 'tangjiong'

import scrapy
from stack_spider.items import QuesItem, TagItem
from stack_spider.utils import parse_int


class StackQuesSpider(scrapy.Spider):
    name = "stack_ques_spider"
    allowed_domains = ["stackoverflow.com"]
    start_urls = ["http://stackoverflow.com/questions"]
    page_size = 50  # 每页的问题数，15 30 50

    # 默认请求第一页，从第一页获取问题总数，方便后续分页
    def parse(self, response):
        # 总问题数，爬到的格式是10,468,983
        ques_count_str = response.css('.summarycount::text').extract()[0]
        # 去掉中间的","号，转成整数
        ques_count_int = int(ques_count_str.replace(',', ''))
        # 总页数
        page_count = ques_count_int / self.page_size + 1
        print '%d questions(%d pages) found!' % (ques_count_int, page_count)
        for index in range(1, page_count):
            print 'starting crawling page %d' % index
            next_page_url = self.start_urls[0] + "?sort=newest&page=" + str(index) + "&pagesize=" + str(self.page_size)
            yield scrapy.Request(next_page_url, callback=self.parse_next_page)

    def parse_next_page(self, response):
        # 每一页的问题 questions_in_single_page
        print 'staring parsing page'
        ques_in_s_p = response.css(".question-summary")
        for ques in ques_in_s_p:
            item = QuesItem()
            item['title'] = ques.css("h3 a::text").extract()[0]
            item['summary'] = ques.css(".excerpt::text").extract()[0]
            item['tags'] = ques.css(".post-tag::text").extract()
            item['timestamp'] = ques.css(".relativetime::attr(title)").extract()[0]
            item['vote_count'] = parse_int(ques.css(".vote .vote-count-post strong::text").extract()[0])
            item['answer_count'] = parse_int(ques.css(".status strong::text").extract()[0])
            item['view_count'] = parse_int(ques.css(".views::text").extract()[0])
            yield item
        print 'parsing page finished'


class StackTagsSpider(scrapy.Spider):
    name = "stack_tags_spider"
    allowed_domains = ["stackoverflow.com"]
    start_urls = ["http://stackoverflow.com/tags"]

    # 默认请求第一页，从第一页获取总页数，方便后续分页
    def parse(self, response):
        # 总页数，这里灵活性比较差，只是比直接把页数写死好一点
        tag_total_page = response.css('.pager a')[4].css('.page-numbers::text').extract()[0]
        print '%s pages tags found!' % tag_total_page
        for index in range(1, int(tag_total_page)):
            print 'starting crawling page %d' % index
            next_page_url = self.start_urls[0] + "?tab=popular&page=" + str(index)
            yield scrapy.Request(next_page_url, callback=self.parse_next_page)

    def parse_next_page(self, response):
        # 每一页的标签 tags_in_single_page
        print 'staring parsing page'
        tags_in_s_p = response.css(".tag-cell")
        for tag in tags_in_s_p:
            item = TagItem()
            item['tagname'] = tag.css(".post-tag::text").extract()[0]
            item['taglink'] = self.allowed_domains[0] + tag.css(".post-tag::attr(href)").extract()[0]
            # 比较靠后的页面，下面的数据可能没有，所以要做判断
            if len(tag.css(".item-multiplier-count::text")) > 0:
                item['questotal'] = parse_int(tag.css(".item-multiplier-count::text").extract()[0])
            else:
                item['questotal'] = 0
            # 页面结构变化大，暂时放弃这个数据
            # item['todayasked'] = parse_int(tag.css(".stats-row a")[0].css('a::text').extract()[0])
            # item['weekasked'] = parse_int(tag.css(".stats-row a")[1].css('a::text').extract()[0])
            yield item
        print 'parsing page finished'
