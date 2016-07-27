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

class ZlzpSpider(CrawlSpider):
    name = "zlzp"
    #allowed_domains = ["www.zhaopin.com/"]
    start_urls = (
        'http://www.zhaopin.com/',
    )

    rules = (
        Rule(LinkExtractor(allow=('jobs.zhaopin.com/[0-9]*\.htm',)),callback='parse_one_job',follow=True),
        Rule(LinkExtractor(allow=('jobs.zhaopin.com/[0-9]*\.html',)),callback='parse_one_job',follow=True),
        Rule(LinkExtractor(allow=('jobs.zhaopin.com/[A-Z0-9]*\.htm',)),callback='parse_one_job',follow=True),
        Rule(LinkExtractor(allow=('zhaopin',),deny=('[a-zA-Z0-9]*/in[0-9]*_','zhaopin.liebiao.com',
                                                    'jobs.zhaopin.com/[a-z]*/[a-z0-9]*/[a-z0-9_]*')),follow=True),
    )

    def parse_one_job(self,response):
        def do_item(item):
            if item and isinstance(item,list):
                return item[0]
            return item

        def parse_jy(jy):
            max_add = 10
            key = "年"
            try:
                if jy.rfind('-'):
                    import re
                    rec=re.compile('([0-9 ]*)-([0-9 ]*)')
                    m = rec.match(jy)
                    if m:
                        low = float(m.group(1))
                        high = float(m.group(2))
                elif jy.rfind('以下'):
                    high =  float(jy[:jy.rfind(key)])
                    low = 0
                elif jy.rfind('以上'):
                    low = float(jy[:jy.rfind(key)])
                    high = low + max_add
                else:
                    low = hight = 0
                avg = (low+high)/2
                return [low,high,avg]
            except Exception as e:
                self.logger.error('a exception jy:%s e:%s',jy,e)
                return [0,0,0]

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
        try:
            items = response.css('ul[class="terminal-ul clearfix"] li')
            item = ZpItem()
            item['url'] = response.url
            item['zwmc'] = do_item(response.css("div[class='fixed-inner-box'] h1::text").extract())
            item['zwyx'] = do_item(items[0].css('strong::text').extract())
            item['gzdd'] = do_item(items[1].css('a::text').extract())
            item['gzjy'] = do_item(items[4].css('strong::text').extract())
            item['xl'] = do_item(items[5].css('strong::text').extract())
            item['zmlb'] = do_item(items[7].css('a::text').extract())
            company_info = response.css('div[class="company-box"]')
            item['gsmc'] = do_item(company_info.css("p[class='company-name-t'] a::text").extract())
            #company_detail = response.css('ul[class="terminal-ul clearfix terminal-company mt20"] li')
            for mc,yx in zip(['yx_low','yx_high','yx_avg'],parse_yx(item['zwyx'])):
                item[mc] = yx
            for mc,jy in zip(['jy_low','jy_high','jy_avg'],parse_yx(item['gzjy'])):
                item[mc] = jy
        except Exception as e:
            self.logger.error("parse url:%s err e:%s",response.url,e)
        #print("fetch a job info:%s from url:%s"%(dict(item),response.url))
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

