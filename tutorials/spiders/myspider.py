__author__ = 'zhangxa'


import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractor import LinkExtractor

class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = [
        Rule(LinkExtractor(allow=('category\.php',),deny=('subsection\.php',))),

        Rule(LinkExtractor(allow=('item\.php',)),callback='parse_item'),
    ]

    def parse_item(self,response):
        self.logger.info('Hi,this is an item page! %s',response.url)

        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item
