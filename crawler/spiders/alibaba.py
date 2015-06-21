# -*- coding: utf-8 -*-
import scrapy


class AlibabaSpider(scrapy.Spider):
    name = "alibaba"
    allowed_domains = ["alibaba.com"]
    start_urls = (
        'http://www.alibaba.com/',
    )

    def parse(self, response):
        pass
