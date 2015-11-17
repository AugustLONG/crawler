#!/usr/bin/python 
# -*- coding: utf-8 -*-
from urlparse import urlparse
import time
import json
import os
import re

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log

from scrapy_ctrip.items import hotelReview

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
    name = 'ctrip'
    # allowed_domains = 'http://hotels.ctrip.com/'
    start_urls = [
        'http://hotels.ctrip.com/Domestic/tool/AjaxGetHotelDetailComment.aspx?MasterHotelID=-1&hotel=690000&card=0&property=0&currentPage=0']

    # callback function when received response
    def parse(self, response):
        # init hotel
        hotel = 0
        # iterate the hotel url
        while hotel < 1:
            if hotel < 10:
                link = response.url.replace(urlparse(response.url)[4].split('&')[1], 'hotel=69000' + str(hotel))
                yield Request(url=link, callback=self.parsePage)
            elif hotel >= 10 and hotel < 100:
                link = response.url.replace(urlparse(response.url)[4].split('&')[1], 'hotel=6900' + str(hotel))
                yield Request(url=link, callback=self.parsePage)
            elif hotel >= 100:
                link = response.url.replace(urlparse(response.url)[4].split('&')[1], 'hotel=690' + str(hotel))
                yield Request(url=link, callback=self.parsePage)
            hotel += 1
        # time.sleep(5)

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

            except:
                page = 0

            for key in range(0, int(page)):
                link = response.url.replace(urlparse(response.url)[4].split('&')[4], 'currentPage=' + str(key))
                print urlparse(response.url)[4].split('&')[4]
                yield Request(url=link, callback=self.parseReview)
                print 'sleep 5 secs'
                time.sleep(5)
        except:
            log.msg("Page Error !!!!! " + response.url, level=log.WARNING)

    def parseReview(self, response):
        sel = Selector(response)
        review_list = []
        hotel_overview = {}
        # hotel profile

        hotel_url = sel.xpath('/html/body/div/div/div/div[2]/a[1]/@href').extract()

        hotel_overview['url'] = 'http://hotels.ctrip.com' + str(hotel_url[0].split('_')[0])
        hotel_overview['total_overall_rating'] = \
            sel.xpath('/html/body/div/div/div/div[1]/div[1]/span[2]/span/text()').extract()[0].strip()

        hotel_overview['per_recomment'] = \
            sel.xpath('/html/body/div/div/div/div[1]/div[1]/span[3]/span/text()').extract()[0].strip()
        hotel_overview['for_biz'] = \
            re.findall(r'\d+', sel.xpath('//*[@id="comment_statistics"]/a[1]/span/text()').extract()[0].strip())[0]
        hotel_overview['for_friend'] = \
            re.findall(r'\d+', sel.xpath('//*[@id="comment_statistics"]/a[2]/span/text()').extract()[0].strip())[0]
        hotel_overview['for_couple'] = \
            re.findall(r'\d+', sel.xpath('//*[@id="comment_statistics"]/a[3]/span/text()').extract()[0].strip())[0]
        hotel_overview['for_family'] = \
            re.findall(r'\d+', sel.xpath('//*[@id="comment_statistics"]/a[4]/span/text()').extract()[0].strip())[0]
        hotel_overview['for_single'] = \
            re.findall(r'\d+', sel.xpath('//*[@id="comment_statistics"]/a[5]/span/text()').extract()[0].strip())[0]
        hotel_overview['for_agent'] = \
            re.findall(r'\d+', sel.xpath('//*[@id="comment_statistics"]/a[6]/span/text()').extract()[0].strip())[0]
        hotel_overview['for_others'] = \
            re.findall(r'\d+', sel.xpath('//*[@id="comment_statistics"]/a[7]/span/text()').extract()[0].strip())[0]

        hotel_overview['avg_location'] = sel.xpath('/html/body/div/div/div/div[1]/div[3]/p[1]/span/text()').extract()[
            0].strip()
        hotel_overview['avg_facility'] = sel.xpath('/html/body/div/div/div/div[1]/div[3]/p[2]/span/text()').extract()[
            0].strip()
        hotel_overview['avg_service'] = sel.xpath('/html/body/div/div/div/div[1]/div[3]/p[3]/span/text()').extract()[
            0].strip()
        hotel_overview['avg_clean'] = sel.xpath('/html/body/div/div/div/div[1]/div[3]/p[4]/span/text()').extract()[
            0].strip()
        hotel_overview['all_comment'] = \
            re.findall(r'\d+', sel.xpath('//*[@id="All_Commnet"]/text()').extract()[0].strip())[0]
        hotel_overview['recomment'] = re.findall(r'\d+', sel.xpath('//*[@id="Recomment"]/text()').extract()[0].strip())[
            0]
        hotel_overview['no_recomment'] = \
            re.findall(r'\d+', sel.xpath('//*[@id="No_Recoment"]/text()').extract()[0].strip())[0]

        review_list.append(dict(hotel_overview))

        try:
            # Number of reviews per page
            num = len(sel.xpath('/html/body/div/div/div/div[3]/text()'))
            # Hotel Profile

            for flag in xrange(1, num):
                # Review
                item = hotelReview()
                print flag
                author = sel.xpath('/html/body/div/div/div/div[3]/div[' + str(flag) + ']/div[1]/p[2]/text()').extract()
                user_type = sel.xpath(
                    '/html/body/div/div/div/div[3]/div[' + str(flag) + ']/div[1]/p[1]/@title').extract()
                date = sel.xpath('/html/body/div/div/div/div[3]/div[' + str(flag) + ']/p/span[3]/a/text()').extract()
                room_type = sel.xpath(
                    '/html/body/div/div/div/div[3]/div[' + str(flag) + ']/div[1]/p[3]/text()').extract()
                review_overall_rating = sel.xpath(
                    '/html/body/div/div/div/div[3]/div[' + str(flag) + ']/p/span[2]/span/text()').extract()
                review_aspect_rating = sel.xpath(
                    '/html/body/div/div/div/div[3]/div[' + str(flag) + ']/p/span[1]/@data-value').extract()
                helpful = sel.xpath(
                    '/html/body/div/div/div/div[3]/div[' + str(flag) + ']/div[2]/a/span/text()').extract()
                review = sel.xpath('/html/body/div/div/div/div[3]/div[' + str(flag) + ']/div[2]/text()').extract()

                # print str(response.body).decode('GB2312').encode('utf8')
                filename = response.url.split('?')[1].split('&')[1].split('=')[1]
                print 'HIIIIIIIIIII'
                print filename
                # item is an object
                item['author'] = author[0].strip()
                item['user_type'] = user_type[0].strip()
                item['date'] = date[0].strip()
                item['room_type'] = room_type[0].strip()
                item['review_overall_rating'] = review_overall_rating[0].strip()
                # """
                # "clean": ["", " ", "卫生：5", " ", "服务：5", " ", "设施：5", " ", "位置：5\r\n", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
                # """
                item['location'] = re.findall(r'\d+', review_aspect_rating[0].strip().split(',')[0])[0]
                item['facility'] = re.findall(r'\d+', review_aspect_rating[0].strip().split(',')[1])[0]
                item['service'] = re.findall(r'\d+', review_aspect_rating[0].strip().split(',')[2])[0]
                item['clean'] = re.findall(r'\d+', review_aspect_rating[0].strip().split(',')[3])[0]
                item['review'] = review[0].strip()
                item['helpful'] = re.findall(r'\d+', helpful[0].strip())[0]

                review_list.append(dict(item))

                print review_list
            # Write the file like the pipe
            con = json.dumps(review_list, ensure_ascii=False).encode('utf8')
            self.writeAppendFile(filename, con)
        except:
            log.msg("Review Error !!!!" + response.url, level=log.WARNING)

    def writeAppendFile(self, filename, con):
        print "write!!!!!!"
        with open(os.path.join('reviews', str(filename)), 'a') as file:
            content = str(con)
            file.write(con)
