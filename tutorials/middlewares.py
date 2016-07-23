__author__ = 'zhangxa'

import time

from selenium import webdriver
from scrapy.http import HtmlResponse

class MyCustomSpiderMiddleware(object):
    def process_request(self, request, spider):
        print("PhantomJS is starting... url:",request.url)
        driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")
        driver.get(request.url)
        time.sleep(3)
        body = driver.page_source
        driver.close()
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
