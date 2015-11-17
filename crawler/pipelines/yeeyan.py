# coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import os
import sqlite3

from scrapy import log
from scrapy import signals
from scrapy.exceptions import *
from scrapy.xlib.pydispatch import dispatcher


class YeeyanPipeline(object):
    file_path = "yeeyan.db"

    def __init__(self):
        self.con = None
        self.cur = None
        self.count = 0
        self.exist_count = 0
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        url = item['url']
        title = item['title']
        author = item['author']
        release_time = item['release_time']
        excerpt = item['excerpt']
        category = item['category']
        jx = False
        if category in [u'译科技', u'译生活', u'译商业', u'译新知']:
            jx = True
        content_html = item['content_html']
        try:
            self.cur.execute('insert into yeeyan values(?,?,?,?,?,?,?,?)',
                             (url, title, author, release_time, excerpt, category, content_html, jx))
        except sqlite3.IntegrityError:
            # log.msg(u'error 文章已存在,%s'%title)
            self.exist_count += 1
            if self.exist_count == 100:
                self.con.commit()
                self.con.close()
                os.abort()
        else:
            self.count += 1
            if self.count == 100:
                self.con.commit()
                self.count = 0
            log.msg('get passage %s,%s' % (title, release_time), level=log.INFO)

    def spider_opened(self):
        if os.path.exists(self.file_path):
            self.con = sqlite3.connect(self.file_path)
            self.cur = self.con.cursor()
        else:
            self.initialize_database()

    def spider_closed(self):
        if self.con:
            self.con.commit()
            self.con.close()
            self.con = None

    def initialize_database(self):
        self.con = sqlite3.connect(self.file_path)
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE yeeyan (url TEXT PRIMARY KEY,title TEXT,
        author TEXT,release_time DATE,excerpt TEXT,category TEXT,content_html TEXT,
        jx TEXT)''')
        self.con.commit()
