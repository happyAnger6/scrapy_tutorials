# -*- coding: utf-8 -*-
import scrapy


class BjljiaSpider(scrapy.Spider):
    name = "bjljia"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = (
        'http://bj.lianjia.com/',
    )

    def parse(self, response):
        print(response.body)
