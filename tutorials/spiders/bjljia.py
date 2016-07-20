# -*- coding: utf-8 -*-
import scrapy

from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import HouseItem,CjHouseItem

class BjljiaSpider(CrawlSpider):
    name = "bjljia"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = (
        'http://bj.lianjia.com/ershoufang/',
        'http://bj.lianjia.com/chengjiao/',
    )

    rules = (
        Rule(LinkExtractor(allow='ershoufang/[0-9]*\.html',),callback='parse_one_house_info',follow=True),
        Rule(LinkExtractor(allow='ershoufang',),follow=True),
        Rule(LinkExtractor(allow='chengjiao/[a-zA-Z0-9]*/',),callback='parse_pg_chengjiao_house_info',follow=True),
        Rule(LinkExtractor(allow='chengjiao/[a-zA-Z0-9]*\.html',),callback='parse_chengjiao_house_info',follow=True),
        Rule(LinkExtractor(allow='chengjiao',),follow=True),

    )

    def parse_pg_chengjiao_house_info(self,response):
        lists = response.css('ul[class="listContent"] li')
        items = []
        for index,list in enumerate(lists):
            item = CjHouseItem()
            item['page_url'] = list.css("a[class='img']::attr(href)").extract()
            item['title'] = list.css("div[class='title'] a::text").extract()
            item['house_info'] = list.css("div[class='houseInfo']::text").extract()
            item['deal_data'] = list.css("div[class='dealDate']::text").extract()
            item['total_price'] = list.css("div[class='totalPrice'] span::text").extract()
            item['position_icon'] =  list.css("div[class='positionInfo']::text").extract()
            item['unit_price'] = list.css("div[class='unitPrice'] span::text").extract()
            item['deal_house_txt'] = list.css("div[class='dealHouseInfo'] span::text").extract()
            item['sell_flag'] = 1
            items.append(item)
        return items

    #分析一个具体房源页面的信息
    def parse_one_house_info(self,response):
        def deal_item(item):
            new_item = HouseItem()
            for key,value in item.items():
                if isinstance(value,list) and value:
                    new_item[key] = value[0]
                else:
                    new_item[key] = value
            return new_item

        item = HouseItem()
        content = response.css("div[class='content']")
        item['page_url'] = response._get_url()
        item['total_price'] =  content.css("span[class='total']::text").extract()
        item['unit_price'] = content.css("span[class='unitPriceValue']::text").extract()
        item['down_payment'] = content.css("div[class='tax'] span::text")[0].extract()
        item['tax'] = content.css("div[class='tax']").css("#PanelTax::text").extract()
        item['house_type'] = content.css("div[class='room']").css("div[class='mainInfo']::text").extract()
        item['house_direction'] = content.css("div[class='type']").css("div[class='mainInfo']::text").extract()
        item['house_layout'] =  content.css("div[class='room']").css("div[class='subInfo']::text").extract()
        item['house_area'] = content.css("div[class='area']").css("div[class='mainInfo']::text").extract()
        item['house_year'] = content.css("div[class='area']").css("div[class='subInfo']::text").extract()
        item['community_name'] =  content.css("div[class='aroundInfo']").css("div[class='communityName']").css("a[class='info']::text").extract()
        item['area_name'] = content.css("a[class='supplement']::text").extract()
        item['school_name'] = content.css("div[class='schoolName']").css("span[style]::text").extract()
        intro_content = response.css("div[class='introContent']")
        item['house_begin_sell'] = intro_content.css("div[class='transaction']").css("div[class='content'] li::text")[0].extract()
        item['house_transacton'] = intro_content.css("div[class='transaction']").css("div[class='content'] li::text")[1].extract()
        item['house_purpose'] = intro_content.css("div[class='transaction']").css("div[class='content'] li::text")[3].extract()
        item['house_full_five'] = intro_content.css("div[class='transaction']").css("div[class='content'] li::text")[4].extract()
        item['house_unique'] = intro_content.css("div[class='transaction']").css("div[class='content'] li::text")[6].extract()
        item['morgage'] = intro_content.css("div[class='transaction']").css("div[class='content'] li::text")[8].extract()
        item['sell_flag'] = 0
        return deal_item(item)
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

