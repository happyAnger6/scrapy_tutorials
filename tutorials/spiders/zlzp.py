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

from ..items import ZlzpItem
class ZlzpSpider(CrawlSpider):
    name = "zlzp"
    #allowed_domains = ["www.zhaopin.com/"]
    start_urls = (
        'http://www.zhaopin.com/beijing/',
        'http://www.highpin.cn/beijing/ci_160200_160400_160000.html',
    )

    rules = (
        Rule(LinkExtractor(allow=('jobs.zhaopin.com/[0-9]*\.htm',)),callback='parse_one_job',follow=True),
        Rule(LinkExtractor(allow=('jobs.zhaopin.com/[0-9]*\.html',)),callback='parse_one_job',follow=True),
        Rule(LinkExtractor(allow=('http://www.highpin.cn/job/h[0-9]*\.htm',)),callback='parse_high_one_job',follow=True),
        Rule(LinkExtractor(allow=('http://www.highpin.cn/job/h[0-9]*\.html',)),callback='parse_high_one_job',follow=True),
        Rule(LinkExtractor(allow=('zhaopin',),deny=('[a-zA-Z0-9]*/in[0-9]*_','zhaopin.liebiao.com',
                                                    'jobs.zhaopin.com/[a-z]*/[a-z0-9]*/[a-z0-9_]*')),follow=True),
    )

    def parse_high_one_job(self,response):
        def do_item(item):
            if item and isinstance(item,list):
                return item[0]
            return item
        items = response.css("ul[class='view-ul view-wid344'] li")
        item = ZlzpItem()
        item['zwmc'] = do_item(response.css("h1 span[class='cursor-d']::text").extract())
        item['zwlb'] = do_item(items[0].css("li::text").extract())
        item['gzdd'] = do_item(items[2].css("a::text").extract())
        item['fbrq'] = do_item(items[3].css("span::text").extract()[1])
        item['zwnx'] = do_item(response.css("li[class='mar-b8'] a::text").extract())
        company_info = response.css('ul[class="view-ul"] li')
        item['gsmc'] = do_item(company_info[0].css('li::text').extract())
        item['gshy'] = do_item(company_info[1].css('li::text').extract())
        item['gsxz'] = do_item(company_info[2].css('li::text').extract())
        item['gsgm'] = do_item(company_info[3].css('li::text').extract())

        print("fetch a job high info:%s from url:%s"%(dict(item),response.url))
        return item

    def parse_one_job(self,response):
        def do_item(item):
            if item and isinstance(item,list):
                return item[0]
            return item
        items = response.css('ul[class="terminal-ul clearfix"] li')
        item = ZlzpItem()
        item['zwyx'] = do_item(items[0].css('strong::text').extract())
        item['gzdd'] = do_item(items[1].css('a::text').extract())
        item['fbrq'] = do_item(items[2].css('span::text').extract()[1])
        item['gzxz'] = do_item(items[3].css('strong::text').extract())
        item['gzjy'] = do_item(items[4].css('strong::text').extract())
        item['zdxl'] = do_item(items[5].css('strong::text').extract())
        item['zwlb'] = do_item(items[7].css('a::text').extract())
        company_info = response.css('div[class="company-box"]')
        item['gsmc'] = do_item(company_info.css("p[class='company-name-t'] a::text").extract())
        company_detail = response.css('ul[class="terminal-ul clearfix terminal-company mt20"] li')
        item_names = ['gsgm','gsxz','gshy','gszy','gsdz']
        css_names = ['strong::text','strong::text','a::text','a::text','strong::text']
        for i,detail in enumerate(company_detail):
            item[item_names[i]] = do_item(detail.css(css_names[i]).extract())
        print("fetch a job info:%s from url:%s"%(dict(item),response.url))
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

