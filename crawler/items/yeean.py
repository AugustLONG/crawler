# coding=utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class YeeyanItem(Item):
    url = Field()
    title = Field()
    author = Field()
    release_time = Field()  # 发布时间
    excerpt = Field()  # 摘要
    category = Field()
    content_html = Field()
