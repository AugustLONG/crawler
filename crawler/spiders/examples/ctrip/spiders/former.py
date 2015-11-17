from urlparse import urlparse
import json

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

from scrapy_ctrip.items import hotelReview

"""
	hotel=441000 - hotel=441507
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
	location = Field()
	facility = Field()
	service = Field()
	clean = Field()
	review = Field()
	helpful = Field()
	user_agent = Field()
"""


class ctripSpider(BaseSpider):
    name = 'ctripp'
    allowed_domains = 'http://www.ctrip.com/'
    start_urls = [
        'http://hotels.ctrip.com/Domestic/tool/AjaxGetHotelDetailComment.aspx?MasterHotelID=-1&hotel=441507&card=0&property=0&currentPage=0']

    # callback function when received response
    def parse(self, response):
        sel = Selector(response)

        one_file = {}
        hotel_profile = {}
        review_obj = {}
        review_list = []
        # Hotel Profile

        # Number of reviews per page
        num = len(sel.xpath('//*[@id="hotelCommentList"]/text()'))
        # Number of pages per hotel
        page_list = len(sel.xpath('/html/body/div/div/div/div[3]/div[1]/text()'))

        # page = sel.xpath('/html/body/div/div/div/div[3]/div[1]/a[' + str(page_list - 2) + ']/span/text()')
        page = str(sel.xpath('/html/body/div/div/div/div[3]/div[1]/a[11]/span/text()')).split(' ')[2].split('\'')[1]
        print page_list - 2
        print page
        for flag in xrange(1, num + 1):
            # Review
            item = hotelReview()

            author = sel.xpath('//*[@id="hotelCommentList"]/li[' + str(flag) + ']/div[1]/p[2]/text()').extract()
            date = sel.xpath('//*[@id="hotelCommentList"]/li[' + str(flag) + ']/div[1]/p[3]/text()').extract()
            room_type = sel.xpath(
                '//*[@id="hotelCommentList"]/li[' + str(flag) + ']/div[2]/div/span[1]/text()').extract()
            total_overall_rating = sel.xpath(
                '//*[@id="hotelCommentList"]/li[' + str(flag) + ']/div[2]/div/span[3]/text()').extract()
            review = sel.xpath('//*[@id="hotelCommentList"]/li[' + str(flag) + ']/div[2]/p[3]/text()').extract()
            helpful = sel.xpath('//*[@id="hotelCommentList"]/li[' + str(flag) + ']/div[2]/p[1]/a/text()').extract()

            # print str(response.body).decode('GB2312').encode('utf8')

            filename = response.url.split('?')[1].split('&')[1].split('=')[1]

            # item is an object
            item['author'] = author[0].strip()
            item['date'] = date[0].strip()
            item['room_type'] = room_type[0].strip()
            item['total_overall_rating'] = total_overall_rating[0].strip()
            item['review'] = review[0].strip()
            item['helpful'] = helpful[0].strip()

            review_list.append(dict(item))

            print len(review_list)

        for key in range(1, 3):
            link = response.url.replace(urlparse(response.url)[4].split('&')[4], 'currentPage=' + str(key))
            print link
            yield Request(
                url="http://hotels.ctrip.com/Domestic/tool/AjaxGetHotelDetailComment.aspx?MasterHotelID=-1&hotel=441507&card=0&property=0&currentPage=1",
                callback=self.parse)

        # Write the file like the pipe
        con = json.dumps(review_list, ensure_ascii=False).encode('utf8')
        self.writeAppendFile(filename, con)

    def writeAppendFile(self, filename, con):
        with open(filename, 'a') as file:
            content = str(con)
            file.write(con)
