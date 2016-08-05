# -*- coding: utf-8 -*-
import scrapy

import time
import re

from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup

from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse

from ..items import SpecItem

class SinaSpeicalSpider(CrawlSpider):
    name = "sina_special"
    #allowed_domains = ["www.51job.com"]
    start_urls = (
        'http://match.2016.sina.com.cn/medals/',
    )

    rules = (
        Rule(LinkExtractor(allow=('2016.sina.com.cn/china/[0-9\-]*/doc-if[a-z0-9]*.shtml',)),callback='parse_one_news',follow=True),
        Rule(LinkExtractor(allow=('2016.sina.com.cn/brazil/[0-9\-]*/doc-if[a-z0-9]*.shtml',
                                  '2016.sina.com.cn/side/[0-9\-]*/doc-if[a-z0-9]*.shtml')),callback='parse_one_news',follow=True),
        Rule(LinkExtractor(allow=('2016.sina.com.cn',),deny=('php$','php?','video.sina.com.cn',
                                                  )),follow=True),
    )

    def parse(self,response):
        def do_item(item):
            if item and isinstance(item,list):
                return item[0]
            return item
        try:
            rows = response.css("table[class='tb_02 tb_04'] tr[class='sub']")

            for row in rows:
                item = SpecItem()
                item['url'] = response.url
                item['kind'] = 1
                item['rank'] = row.css("td[class='w01'] ::text").extract()[0].strip()
                item['country'] = row.css("td[class='w02'] a::text").extract()[0].strip()
                item['gold'] = row.css("td[class='w03'] a::text").extract()[0].strip()
                item['silver'] = row.css("td[class='w04'] a::text").extract()[0].strip()
                item['bronze'] = row.css("td[class='w05'] a::text").extract()[0].strip()
                item['total'] = row.css("td[class='w06'] a::text").extract()[0].strip()
                yield item

        except Exception as e:
            self.logger.error("parse url:%s err:%s",response.url,e)
            return []
        return item


"""
    def parse_page(self,response):
        print("aaaaaaaaaaaaaaaaa",response.url)
        links = response.css('a::attr(href)').extract()
        for link in [ link for link in links if link.startswith('http:') ]:
            yield scrapy.Request(url=link,callback=self.parse_page)

    def parse(self, response):
        print("parse url:%s"%response.url)

    def parse_url(self,response):
        links = response.css('a::attr(href)').extract()
        for link in [ link for link in links if link.startswith('http:') ]:
            yield scrapy.Request(url=link,callback=self.parse_url)

    #这个方法的优先级大于start_urls,会优先用这个构造初始requests
    def start_requests(self):
        print("this method has high priority than start_urls")
        yield scrapy.Request('http://bj.lianjia.com/ershoufang/',self.parse)


    #当指定了start_urls时，这个方法会被用于创建Request对象.
    def make_requests_from_url(self, url):
        print("url:",url,"make_requests_from_url")
        return scrapy.Request(url,callback=self.parse)
    """

