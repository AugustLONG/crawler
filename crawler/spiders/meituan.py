# -*- coding: utf-8 -*-
import scrapy


class MeituanSpider(scrapy.Spider):
    name = "meituan"
    allowed_domains = ["meituan.com"]
    start_urls = (
        'http://www.meituan.com/',
    )

    def parse(self, response):
        pass
