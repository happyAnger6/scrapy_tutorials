__author__ = 'zhangxa'

import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from ghost import Ghost

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http.response.html import HtmlResponse

from ..items import NewsItem

class GhostSinaSpider(CrawlSpider):
    def __init__(self,*a,**kw):
        super(GhostSinaSpider,self).__init__(*a,**kw)


    name = "sina_oly_ghost"
    #allowed_domains = ["www.51job.com"]
    start_urls = (
        'http://2016.sina.com.cn/',
    )

    rules = (
        Rule(LinkExtractor(allow=('2016.sina.com.cn/china/[0-9\-]*/doc-if[a-z0-9]*.shtml',)),process_request='ghost_process',callback='parse_one_news',follow=True),
        Rule(LinkExtractor(allow=('2016.sina.com.cn/brazil/[0-9\-]*/doc-if[a-z0-9]*.shtml',
                                  '2016.sina.com.cn/side/[0-9\-]*/doc-if[a-z0-9]*.shtml')),
                                    process_request='phantomjs_process',callback='parse_one_news',follow=True),
        Rule(LinkExtractor(allow=('2016.sina.com.cn',),deny=('php$','php?','video.sina.com.cn',
                                                  )),follow=True),
    )


    def parse_one_news(self,response):
        def do_item(item):
            content = item
            if item and isinstance(item,list):
                content = item[0]
            if content:
                return content.strip()
            return ""

        item = NewsItem()
        try:
            item['url'] = response.url
            item['title'] = do_item(response.css("h1[id='j_title'] ::text").extract())
            item['publish'] = do_item(response.css("span[class='article-a__time'] ::text").extract())
            item['pic_title'] = do_item(response.css("figcaption[class='article-a__figcaption'] ::text").extract())
            keywords_lst = []
            keywords =  response.css("section[class='article-a_keywords'] a")
            for word in keywords:
                keywords_lst.append(word.css("a::text").extract()[0])
            item['keywords'] = keywords_lst
            print("ddd",response.css("div[id='j_commentlist'] span[class='count'] a::text").extract())
            counts = response.css("p[class='post_box_count'] span[class='f_red']::text").extract()
            item['involves'] = counts[1].replace(',','')
            item['comments'] = counts[0].replace(',','')
            item['hot'] = float(item['involves'])*0.3 + float(item['comments'])*0.7
            '''
            filename = response.url.split("/")[-2] + '.html'
            with open(filename,'wb') as f:
                f.write(response.body)
            '''
        except Exception as e:
            self.logger.error("parse url:%s err:%s",response.url,e)
            return []
        return item

    def ghost_process(self,request):
        def do_counts(str_counts):
            try:
                counts = str_counts.replace(',','')
                return counts
            except:
                return 0
        def do_item(item):
            if item and isinstance(item,list):
                return item[0]
            return item
        url = request.url
        try:
            ghost = Ghost()
            with ghost.start() as session:
                page,extra_resouce = session.open(url)
            response = HtmlResponse(url,body=page.content.encode('UTF-8'),request=request)
        except Exception as e:
            self.logger.error("ghost.py error:",e,url)
            return []
        return self.parse_one_news(response)