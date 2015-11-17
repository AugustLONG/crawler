# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    logo_url = scrapy.Field()
    price = scrapy.Field()
    detile_url = scrapy.Field()
    next_url = scrapy.Field()
    saleCount = scrapy.Field()
    addressPoint = scrapy.Field()
    ticket_title = scrapy.Field()
    introduce = scrapy.Field()
    detil_title = scrapy.Field()
    img_path = scrapy.Field()


class webProxy(scrapy.Item):
    proxy = scrapy.Field()
