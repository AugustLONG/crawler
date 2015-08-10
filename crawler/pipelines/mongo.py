# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import logging
from scrapy import signals
from scrapy.exceptions import *
from scrapy.conf import settings
from crawler.settings import MONGO_HOST
from scrapy.xlib.pydispatch import dispatcher
import pymongo
from bson.objectid import ObjectId
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class MongoPipeline(object):
    port = 27017

    def __init__(self):
        self.conn = None
        self.db = None
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        site = item['site']
        collection = self.db[site]
        url = item['url']
        old_item = collection.find_one({"url": url},["url", "_id"])
        if old_item:
            item["_id"] = old_item["_id"]
            collection.save(item)
        else:
            collection.insert(item)
        logging.info('get passage %s' % site)
        return item

    def spider_opened(self):
        self.conn = pymongo.MongoClient(MONGO_HOST, self.port)
        self.db = self.conn.crawler
        # db.authenticate("tage","123")

    def spider_closed(self):
        if self.conn:
            self.conn.close()
            self.conn = None
