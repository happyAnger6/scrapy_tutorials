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

class LaGouSpider(CrawlSpider):
    name = "lagou"
    allowed_domains = ["www.lagou.com"]

    '''
    start_urls = (
        'http://www.lagou.com/',
    )
    '''

    rules = (
        Rule(LinkExtractor(allow=('lagou',),deny=('[a-zA-Z0-9]*/in[0-9]*_','zhaopin.liebiao.com',
                                                    'jobs.zhaopin.com/[a-z]*/[a-z0-9]*/[a-z0-9_]*')),callback='parse_one_page',follow=True),
    )

    def __init__(self, *a, **kw):
        super(LaGouSpider, self).__init__(*a, **kw)
        self.driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")

    def start_requests(self):
        return [scrapy.FormRequest("https://passport.lagou.com/login/login.html",
                                   formdata={'user':'18600146108','pass':'168888'},
                                   callback=self.logged_in)]

    def logged_in(self,response):
        self.down_to_file(response.url,response.body)

    def closed(self,reason):
        self.driver.close()

    def parse_page_info(self,response):
        print("reponse",response)

    def make_requests_from_url(self, url):
        return scrapy.Request(url,callback=self.parse)

    def parse_one_page(self,response):
        print("parse_one_page",response.url)
        self.down_to_file(response.url,response.body)

    def down_to_file(self,url,body):
        filename = url.split("/")[-2] + '.html'
        with open(filename,'wb') as f:
            f.write(body)

    def parse_start_url(self, response):
        url = response.url
        print("phantomjs is starting.....")
        driver = self.driver
        driver.get(url)
        body = driver.page_source
        bs = BeautifulSoup(body)
        tags = bs.findAll(href=re.compile(".*"))
        urls = []
        for tag in tags:
            urls.append(tag.attrs['href'])
        for url in urls:
            if url.startswith('http:'):
                yield scrapy.Request(url=url,callback=self.parse_one_page)


"""
    def parse(self, response):
        #print("parse url:%s"%response.url)
        links = response.css('a::attr(href)').extract()
        for link in [ link for link in links if link.startswith('http:') ]:
            yield scrapy.Request(url=link,callback=self.parse_url)

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

