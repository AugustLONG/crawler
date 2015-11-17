#!/usr/bin/python 
# -*- coding: utf-8 -*-
from urlparse import urlparse
import time
import json
import os

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log

check = []
"""
	hotel=441007 - hotel=441507
"""
"""
    #hotel profile
	hotel_name = Field()
	e_name = Field()
	avg_price = Field()
	url = Field()
	total_overall_rating = Field()
	avg_location = Field()
	avg_facility = Field()
	avg_service = Field()
	avg_clean = Field()
	all_comment = Field()
	recomment = Field()
	no_recomment = Field()

	#review
	author = Field()
	user_type = Field()
	date = Field()
	room_type = Field()
	review_overall_rating = Field()
	clean = Field()
	service = Field()	
	facility = Field()
	location = Field()
	review = Field()
	helpful = Field()
	user_agent = Field()
"""


class ctripSpider(BaseSpider):
    name = 'check'
    # allowed_domains = 'http://hotels.ctrip.com/'

    start_urls = [
        'http://hotels.ctrip.com/Domestic/tool/AjaxGetHotelDetailComment.aspx?MasterHotelID=-1&hotel=42900&card=0&property=0&currentPage=0']


    # callback function when received response
    def parse(self, response):
        # init hotel
        hotel = 0
        # iterate the hotel url
        while hotel < 1000:
            if hotel < 10:
                link = response.url.replace(urlparse(response.url)[4].split('&')[1], 'hotel=42900' + str(hotel))
                yield Request(url=link, callback=self.parsePage, meta={'hotel': hotel})
            elif hotel >= 10 and hotel < 100:
                link = response.url.replace(urlparse(response.url)[4].split('&')[1], 'hotel=4290' + str(hotel))
                yield Request(url=link, callback=self.parsePage, meta={'hotel': hotel})
            elif hotel >= 100:
                link = response.url.replace(urlparse(response.url)[4].split('&')[1], 'hotel=429' + str(hotel))
                yield Request(url=link, callback=self.parsePage, meta={'hotel': hotel})
            hotel += 1
        # time.sleep(5)
        print check

    def parsePage(self, response):
        sel = Selector(response)

        try:
            try:
                # Number of pages per hotel
                page_list = len(sel.xpath('/html/body/div/div/div/div[4]/div/div[1]/text()'))
                page = str(sel.xpath(
                    '/html/body/div/div/div/div[4]/div/div[1]/a[' + str(page_list - 2) + ']/span/text()')).split(' ')[
                    2].split('\'')[1]
                print "page_list!!!"
                print page_list - 2
                print page
                if int(page) >= 74:
                    print "get!"
                    check.append(response.meta['hotel'])
                    con = json.dumps(check, ensure_ascii=False).encode('utf8')
                    print con
                    f = open('check', 'r+')
                    f.write(con)

            except:
                page = 0
                print "let page == 0"

            print 'sleep 5 secs'
            time.sleep(5)
        except:
            log.msg("Page Error !!!!! " + response.url, level=log.WARNING)

    def writeAppendFile(self, filename, con):
        with open(os.path.join('reviews', str(filename)), 'a') as file:
            content = str(con)
            file.write(con)
