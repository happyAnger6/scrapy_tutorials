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
class WyjobSpider(CrawlSpider):
    name = "wyjob"
    #allowed_domains = ["www.51job.com"]
    start_urls = (
        'http://www.51job.com/beijing',
    )

    rules = (
        Rule(LinkExtractor(allow=('jobs.51job.com/beijing-[a-z\-]*/[0-9]*\.htm',)),callback='parse_one_job',follow=True),
        Rule(LinkExtractor(allow=('jobs.51job.com/hot/[0-9\-]*\.htm',)),callback='parse_one_job',follow=True),
        Rule(LinkExtractor(allow=('jobs.51job.com/beijing/p[0-9]*/',),deny=('php$','php?'
                                                  ,'search.51job.com',
                                                  )),follow=True),
    )

    def parse_one_job(self,response):
        def do_item(item):
            if item and isinstance(item,list):
                return item[0]
            return item

        def parse_yx(yx):
            max_add = 10000
            try:
                if yx.rfind('-'):
                    import re
                    rec=re.compile('([0-9 ]*)-([0-9 ]*)')
                    m = rec.match(yx)
                    if m:
                        low = float(m.group(1))
                        high = float(m.group(2))
                elif yx.rfind('以下'):
                    high =  float(yx[:yx.rfind("元")])
                    low = 0
                elif yx.rfind('以上'):
                    low = float(yx[:yx.rfind("元")])
                    high = low + max_add
                else:
                    low = hight = 0
                avg = (low+high)/2
                return [low,high,avg]
            except Exception as e:
                self.logger.error('a exception yx:%s e:%s',yx,e)
                return [0,0,0]

        item = ZpItem()
        try:
            cn = response.css("div[class='cn']")
            item['url'] = response.url
            item['zwyx'] = do_item(cn.css("strong::text").extract())
            item['gsxz'] = do_item(cn.css("p[class='msg ltype']::text").extract())
            item['gzdd'] = do_item(cn.css("span[class='lname']::text").extract())
            item['zwmc'] = do_item(cn.css("h1::text").extract())
            item['gsmc'] = do_item(cn.css("p[class='cname'] a::text").extract())

            for mc,yx in zip(['yx_low','yx_high','yx_avg'],parse_yx(item['zwyx'])):
                item[mc] = yx
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

