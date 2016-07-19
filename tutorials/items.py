# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    

class HouseItem(scrapy.Item):
    total_price = scrapy.Field() #总价
    unit_price = scrapy.Field() #单价
    down_payment = scrapy.Field() #首付
    tax = scrapy.Field() #税费
    house_type = scrapy.Field()  #居室
    house_year = scrapy.Field()
    house_layout = scrapy.Field() #楼层
    house_direction = scrapy.Field() #朝向
    house_decorate = scrapy.Field() #装修
    house_area = scrapy.Field() #面积
    house_fact_area = scrapy.Field() #实际面积
    house_begin_sell = scrapy.Field() #挂牌时间
    house_purpose = scrapy.Field() #房屋用途
    house_transacton = scrapy.Field() #交易权属
    house_full_five = scrapy.Field() #满5年
    house_unique = scrapy.Field() #是否唯一
    community_name = scrapy.Field() #小区名称
    area_name = scrapy.Field() #地理位置
    school_name = scrapy.Field() #学校
    morgage = scrapy.Field() #是否抵押
    page_url = scrapy.Field()


