# -*- coding: utf-8 -*-
'''
Created on 2015-11-22
@author: 李飞飞
'''

import os
import time
from scrapy.spiders import Spider
from scrapy.http.request import Request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class WeiboSpider(Spider):
    name = "weibo"
    allowed_domains = ["weibo.com"]

    cookie = None

    start_urls = [
        "http://weibo.com",
    ]

    def __init__(self):
        chromedriver = "/home/dash/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        login_url = "http://weibo.com/login.php?url=http%3A%2F%2Fweibo.com%2Fu%2F3655689037%2Fhome%3Fleftnav%3D1%26wvr%3D5"
        browser = webdriver.Chrome(chromedriver)
        browser.get(login_url)
        time.sleep(5)
        usernamebox = browser.find_element_by_xpath("//div[@class='inp username']/input")  # Find the search box
        passwordbox = browser.find_element_by_xpath("//div[@class='inp password']/input")  # Find the search box
        usernamebox.send_keys('cisl20140001@126.com')
        passwordbox.send_keys('dash123456'+Keys.RETURN)
        print 'go to '
        time.sleep(8)
        print 'ready to get cookie'
        self.cookie = browser.get_cookies()
        print self.cookie;

    def start_requests(self):
        return [Request(url=self.start_urls[0], method='get',cookies=self.cookie,callback=self.showhtml)]

    def showhtml(self , response):
#       print 'body'
#      print response.body
        with open('%s%s%s' % (os.getcwd(), os.sep, 'fetch.html'), 'wb') as f:
            f.write(response.body)