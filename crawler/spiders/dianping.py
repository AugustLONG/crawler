# -*- coding: utf-8 -*-
import scrapy


class DianpingSpider(scrapy.Spider):
    name = "dianping"
    allowed_domains = ["dianping.com"]
    start_urls = (
        'http://www.dianping.com/',
    )

    def parse(self, response):
        pass
