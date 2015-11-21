# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

from crawler.items.dmoz import DmozItem


def change_word(s):
    sum = 0
    for i in s[0]:
        sum += 1
    ss2 = ''

    for i in range(0, sum):
        if (s[0][i] == u'\u2014'):
            continue
        ss2 += s[0][i]

    s = ss2
    print s
    return s


class A51newrenSpider(scrapy.Spider):
    name = "51newren"
    allowed_domains = ["51newren.com"]
    start_urls = (
        'http://www.51newren.com/Login',
    )

    def __init__(self, *args, **kwargs):
        super(A51newrenSpider, self).__init__(*args, **kwargs)
        self.http_user = "fanfzj"
        self.http_pass = "6yhn6yhn"
        self.http_type = "User"
        self.formdata = {'UserType': self.http_type, \
                         'Username': self.http_user, \
                         'Password': self.http_pass, \
                         }
        self.headers = {'ccept-Charset': 'GBK,utf-8;q=0.9,*;q=0.8', \
                        'Accept-Encoding': 'gzip,deflate,sdch', \
                        'Accept-Language': 'zh-CN,zh;q=0.8', \
                        'Cache-Control': 'max-age=0', \
                        'Connection': 'keep-alive', \
                        'Cookie': 'ASP.NET_SessionId=byctjwgamtav5oarxn2p24xi; __RequestVerificationToken=BSDY33UtJXv0XqMkIvAJXAdMXC-jqACBsiZb6-mx4uW8Hr89aArTh9DfLtQFDh6NwQsqHXiZMTzheuim3ETI78PhOzQf263wliXL8ArkTrA1; .ASPXAUTH=510AC9FF4C4DA8D453D8A4335D3D9DB941560D23AFA4C1C01C2721DDF6B9FBFA225842EABD511656CA9C43509DC5984CE291D471F509A146999A24162CEFBB9CF4034E48FEC29959D07B0EE8966B54D19DBE75D9625A4D5C1750245906633942; CNZZDATA1256053577=1130977004-1442210868-%7C1442210868'
                        }
        self.id = 0

    def parse(self, response):
        sel = scrapy.Selector(response)
        item = DmozItem()
        sel = scrapy.Selector(response)
        href = str(response.url)
        hidden = sel.xpath("//input[@name='__RequestVerificationToken']/@value").extract()
        return [FormRequest.from_response(response, \
                                          formdata=self.formdata, \
                                          headers=self.headers, \
                                          meta={
                                              '__RequestVerificationToken': 'BSDY33UtJXv0XqMkIvAJXAdMXC-jqACBsiZb6-mx4uW8Hr89aArTh9DfLtQFDh6NwQsqHXiZMTzheuim3ETI78PhOzQf263wliXL8ArkTrA1'}, \
                                          callback=self.parse_item)]

    def parse_item(self, response):
        sel = scrapy.Selector(response)
        print sel.xpath("//span[@class=' user_name_show']/text()").extract()
