__author__ = 'zhangxa'

import time

from selenium import webdriver
from scrapy.http import HtmlResponse

class MyCustomSpiderMiddleware(object):
    def process_request(self, request, spider):
        print("PhantomJS is starting... url:",request.url)
        time.sleep(1)
