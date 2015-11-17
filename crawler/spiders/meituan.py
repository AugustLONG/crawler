# -*- coding: utf-8 -*-
import logging
from xml.dom import minidom

import scrapy
from scrapy.utils.iterators import xmliter
from scrapy.utils.spider import iterate_spider_output

from crawler.utils.xml import get_attrvalue, get_nodevalue, get_xmlnode

logger = logging.getLogger("MeituanSpider")
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class MeituanSpider(scrapy.Spider):
    name = "meituan"
    allowed_domains = ["meituan.com"]

    def start_requests(self):
        # yield scrapy.Request('http://www.meituan.com/api/v1/divisions', self.parse_cities)
        yield scrapy.Request('http://api.union.meituan.com/data/hao123v2/key/49728f4253a49bc61208705a8320a27e997/new',
                             self.parse_hao123)
        yield scrapy.Request('http://api.union.meituan.com/data/tuan800/key/49728f4253a49bc61208705a8320a27e997/new',
                             self.parse_tuan800)

    def parse_cities(self, response):
        nodes = xmliter(response, "division")
        for selector in nodes:
            ret = iterate_spider_output(self.parse_city(response, selector))
            for result_item in ret:
                yield result_item

    def parse_city(self, response, nodes):
        name = nodes.xpath('name/text()').extract()[0]
        chart = nodes.xpath('id/text()').extract()[0]
        # print chart
        timezone = nodes.xpath('location/timezone/text()').extract()[0]
        timezone_offset_gmt = nodes.xpath('location/timezone_offset_gmt/text()').extract()[0]
        latitude = nodes.xpath('location/latitude/text()').extract()[0]
        longitude = nodes.xpath('location/longitude/text()').extract()[0]
        url = "http://api.union.meituan.com/data/hao123v2/key/49728f4253a49bc61208705a8320a27e997/city/" + chart
        yield scrapy.Request(url, callback=self.parse_hao123)
        url = "http://api.union.meituan.com/data/tuan800/key/49728f4253a49bc61208705a8320a27e997/city/" + chart
        yield scrapy.Request(url, callback=self.parse_tuan800)

    def parse_hao123(self, response):
        dom = minidom.parseString(response.body)
        root = dom.documentElement
        roots = get_xmlnode(root, 'url')
        for root in roots:
            url = get_xmlnode(root, 'loc')[0].childNodes[0].nodeValue
            url = url.split('&url=')[1]
            id = url.split("/")[-1].replace(".html", "")
            item = {"site": "meituan", "shops": [], "url": url, "id": id, "apiType": "hao123"}
            display_nodes = get_xmlnode(root, 'display')[0].childNodes
            for display in display_nodes:
                if display.nodeName == "#text":
                    continue
                elif display.nodeName == "shops":
                    shop_nodes = get_xmlnode(display, 'shop')
                    shop = {}
                    for shop_node in shop_nodes:
                        for node in shop_node.childNodes:
                            if node.nodeName == "#text":
                                continue
                            elif node.childNodes:
                                shop[node.nodeName] = node.childNodes[0].nodeValue  # wholeText
                    item["shops"].append(shop)
                elif display.childNodes:
                    item[display.nodeName] = display.childNodes[0].nodeValue  # wholeText
            yield item

    def parse_tuan800(self, response):
        dom = minidom.parseString(response.body)
        root = dom.documentElement
        roots = get_xmlnode(root, 'url')
        for root in roots:
            url = get_xmlnode(root, 'loc')[0].childNodes[0].nodeValue
            id = url.split("/")[-1].replace(".html", "")
            item = {"site": "meituan", "shops": [], "url": url, "id": id, "apiType": "tuan800"}
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
