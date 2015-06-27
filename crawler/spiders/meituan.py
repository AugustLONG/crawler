# -*- coding: utf-8 -*-
import scrapy
import logging
logger = logging.getLogger("MeituanSpider")
from scrapy.spiders import XMLFeedSpider

class MeituanSpider(XMLFeedSpider):
    name = "meituan"
    allowed_domains = ["meituan.com"]
    start_urls = (
        'http://www.meituan.com/api/v1/divisions',
    )
    iterator = 'iternodes'
    itertag = 'division'


    def parse_node(self, response, node):
        logger.info('Hi, this is a <%s> node!: %s' % (self.itertag, ''.join(node.extract())))
        print node
        print node.xpath('name/text()').extract()
        print node.xpath('id/text()').extract()
        print node.xpath('id/text()').extract()
        print node.xpath('id/text()').extract()
        print node.xpath('id/text()').extract()
        print node.xpath('id/text()').extract()
        print node.xpath('id/text()').extract()
        print node.xpath('id/text()').extract()
        # print node.xpath('name/text()').extract()[0]
        # print node.xpath('description/text()').extract()
        # for url in response.xpath('//a/@href').extract():
        #     yield scrapy.Request(url, callback=self.parse_cities)


    def parse_cities(self, response, nodes):
        print response
        pass

    def parse_city_new(self, response, nodes):
        print response
        pass


