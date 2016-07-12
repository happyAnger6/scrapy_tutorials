# -*- coding: utf-8 -*-
import scrapy


class BjljiaSpider(scrapy.Spider):
    name = "bjljia"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = (
        'http://bj.lianjia.com/',
    )

    def parse(self, response):
        #print("parse url:%s"%response.url)
        links = response.css('a::attr(href)').extract()
        for link in [ link for link in links if link.startswith('http:') ]:
            yield scrapy.Request(url=link,callback=self.parse_url)

    def parse_url(self,response):
        links = response.css('a::attr(href)').extract()
        for link in [ link for link in links if link.startswith('http:') ]:
            yield scrapy.Request(url=link,callback=self.parse_url)