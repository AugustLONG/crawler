# -*- coding: utf-8 -*-
import scrapy
from src.items import SrcItem


class XroxySpider(scrapy.Spider):
    name = "xroxy"
    allowed_domains = ["xrory.com"]
    start_urls = (
        'http://www.xroxy.com/proxylist.htm',
    )

    def parse(self, response):
        table = response.xpath('/html/body/div[1]/div[2]/table[1]')
        self.log(table)
        for tr in table:
			item = SrcItem()
			item['ip'] = tr.xpath('//table/tr/td[2]/a/text()').extract()
			yield item