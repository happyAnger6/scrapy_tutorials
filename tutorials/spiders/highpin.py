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

from ..items import ZpItem

class HighpinSpider(CrawlSpider):
    name = "highpin"
    #allowed_domains = ["www.zhaopin.com/"]
    start_urls = (
        'http://www.highpin.com',
    )

    rules = (
        Rule(LinkExtractor(allow=('http://www.highpin.cn/job/[a-z0-9]*\.htm',)),callback='parse_high_one_job',follow=True),
        Rule(LinkExtractor(allow=('http://www.highpin.cn/job/[a-z0-9]*\.html',)),callback='parse_high_one_job',follow=True),
        Rule(LinkExtractor(allow=('highpin',)),follow=True),
    )

    def parse_high_one_job(self,response):
        def do_item(item):
            if item and isinstance(item,list):
                return item[0]
            return item
        try:
            items = response.css("ul[class='view-ul view-wid344'] li")
            item = ZpItem()
            item['url'] = response.url
            item['zwmc'] = do_item(response.css("span[class='cursor-d']::attr(title)").extract())
            if not item['zwmc']:
                item['zwmc'] = do_item(response.css("span[class='cursor-d ']::attr(title)").extract())
            item['zwlb'] = do_item(items[0].css("li::text").extract())
            item['gzdd'] = do_item(items[2].css("a::text").extract())
            item['fbrq'] = do_item(items[3].css("span::text").extract()[1])
            item['zwnx'] = do_item(response.css("li[class='mar-b8'] a::text").extract())
            company_info = response.css('ul[class="view-ul"] li')

            item['gsmc'] = do_item(company_info[0].css('a::text').extract())
            if not item['gsmc']:
                item['gsmc'] = do_item(company_info[0].css('li::text').extract())

            item['gshy'] = do_item(company_info[1].css('span::attr(title)').extract())
            if not item['gshy']:
                item['gshy'] = do_item(company_info[1].css('li::text').extract())

            item['gsxz'] = do_item(company_info[2].css('li::text').extract())
            item['gsgm'] = do_item(company_info[3].css('li::text').extract())
        except Exception as e:
            self.logger.error("fetch error url:%s e:%s",response.url,e)

        print("fetch a job high info:%s from url:%s"%(dict(item),response.url))
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

