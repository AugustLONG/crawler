# -*- coding: utf-8 -*-
import logging
from xml.dom import minidom

import scrapy
from scrapy.utils.iterators import xmliter
from scrapy.utils.spider import iterate_spider_output

from crawler.utils.xml import get_xmlnode

logger = logging.getLogger("DianpingtuanSpider")
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class DianpingtuanSpider(scrapy.Spider):
    name = "dianpingtuan"
    allowed_domains = ["dianping.com"]

    def start_requests(self):
        yield scrapy.Request('http://api.t.dianping.com/n/base/cities.xml',
                             self.parse_cities)

    def parse_cities(self, response):
        nodes = xmliter(response, "city")
        for selector in nodes:
            ret = iterate_spider_output(self.parse_city(response, selector))
            for result_item in ret:
                yield result_item

    def parse_city(self, response, nodes):
        name = nodes.xpath('name/text()').extract()[0]
        pk = nodes.xpath('id/text()').extract()[0]
        enname = nodes.xpath('enname/text()').extract()[0]
        url = "http://api.t.dianping.com/n/napi.xml?cityId=" + pk
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        dom = minidom.parseString(response.body)
        root = dom.documentElement
        roots = get_xmlnode(root, 'url')
        for root in roots:
            url = get_xmlnode(root, 'loc')[0].childNodes[0].nodeValue
            id = url.split("/")[-1].strip()
            item = {"site": "dianping", "shops": [], "url": url, "id": id, "apiType": "tuan800"}
            display_nodes = get_xmlnode(root, 'display')[0].childNodes
            for display in display_nodes:
                if display.nodeName == "#text":
                    continue
                elif display.childNodes:
                    item[display.nodeName] = display.childNodes[0].nodeValue  # wholeText
            shops_nodes = get_xmlnode(root, 'shop')
            for shop_node in shops_nodes:
                shop = {}
                for node in shop_node.childNodes:
                    if node.nodeName == "#text":
                        continue
                    elif node.childNodes:
                        shop[node.nodeName] = node.childNodes[0].nodeValue  # wholeText
                item["shops"].append(shop)
            yield item
