# -*- coding: utf-8 -*- #
"""
Created on 2015-11-22
@author: 李飞飞
"""
"""
Scrapy项目，抓取国家统计局区划代码，并用D3.js可视化
抓取[国家统计局统计用区划代码](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/)，得到2009-2013五年的统计用区划代码，以2013年为例：
layer |count(code)| name
------|-----------|------------
1     | 31        | 省/市/自治区
2     | 345       | 市
3     | 2856      | 县/区
4     | 43854     | 乡/镇/街道
5     | 694688    | 村/居委会

## 可视化
Demo：[http://phyng.com/scrapy-stats/](http://phyng.com/scrapy-stats/)
"""
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from crawler.items.gov import *


class GovStatsSpider(CrawlSpider):
    name = 'govstats'
    allowed_domains = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/']
    rules = (
        #处理省级列表
        Rule(LinkExtractor(allow=(r'tjyqhdmhcxhfdm/20\d\d/index\.html')), callback='Layer01_Parse'),
        )

    def Layer01_Parse(self, response):

        item = Layer01_Item()
        for i in LinkExtractor(allow=(r'tjyqhdmhcxhfdm/20\d\d/\d\d\.html')).extract_links(response):
            url = i.url
            text = i.text
            item['year'] = url[-12:-8]
            item['name'] = text
            item['code'] = url[-7:-5]
            yield item
            yield Request(url, callback=self.Layer02_Parse)


    def Layer02_Parse(self, response):
        text = response.xpath('/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table')\
               [0].extract()
        item = Layer02_Item()
        item['year'] = re.findall(r'dm/20\d\d', response.url)[0][3:]
        for code, name in re.findall(r'href="\d\d/(\d{4})\.html">([^\d]+?)</a>', text):
            item['name'] = name
            item['code'] = code
            yield item
        for i in LinkExtractor(allow=(r'tjyqhdmhcxhfdm/20\d\d/\d\d/\d{4}\.html')).extract_links(response):
            url = i.url
            text = i.text
            yield Request(url, callback=self.Layer03_Parse)

    def Layer03_Parse(self, response):
        text = response.xpath('/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table')\
               [0].extract()
        item = Layer03_Item()
        item['year'] = re.findall(r'dm/20\d\d', response.url)[0][3:]
        for code, name in re.findall(r'href="\d\d/(\d{6})\.html">([^\d]+?)</a>', text):
            item['name'] = name
            item['code'] = code
            yield item
        for i in LinkExtractor(allow=(r'tjyqhdmhcxhfdm/20\d\d/\d\d/\d\d/\d{6}\.html')).extract_links(response):
            url = i.url
            text = i.text
            yield Request(url, callback=self.Layer04_Parse)

    def Layer04_Parse(self, response):
        text = response.xpath('/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table')\
               [0].extract()
        item = Layer04_Item()
        item['year'] = re.findall(r'dm/20\d\d', response.url)[0][3:]
        for code, name in re.findall(r'href="\d\d/(\d{9}).html">([^\d]+?)</a>', text):
            item['name'] = name
            item['code'] = code
            yield item
        for i in LinkExtractor(allow=(r'tjyqhdmhcxhfdm/20\d\d/\d\d/\d\d/\d\d/\d{9}\.html')).extract_links(response):
            url = i.url
            text = i.text
            yield Request(url, callback=self.Layer05_Parse)

    def Layer05_Parse(self, response):
        text = response.xpath('/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table')\
               [0].extract()
        item = Layer05_Item()
        item['year'] = re.findall(r'dm/20\d\d', response.url)[0][3:]
        for code, code2, name in re.findall(r'<td>(\d{12})</td><td>(\d\d\d)</td><td>(.+?)</td>', text):
            item['name'] = name
            item['code'] = code
            item['code2'] = code2
            yield item