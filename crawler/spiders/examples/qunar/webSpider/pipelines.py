# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os.path
import os
import urllib2

import scrapy
from scrapy.http import Request
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

from webSpider.settings import PROXY_LIST


def change(sr, tart):
    s = tart.split('.')
    s[0] = sr
    return '.'.join(s)


class WebspiderPipeline(object):
    def __init__(self):
        # files = os.path.join(TOP_DIR,'proxyList.txt')
        # self.files = settings.get('PROXY_LIST')

        self.file = open(PROXY_LIST, 'a')

    def __proxy(self, line):
        # print line
        if '//' in line:
            p = "%s" % line
            htt = line.split(':')[0]
        else:
            p = "http://%s" % line
            htt = "http"
        h = urllib2.ProxyHandler({htt: p})
        o = urllib2.build_opener(h, urllib2.HTTPHandler)
        try:
            r = o.open("http://www.baidu.com/", timeout=3)
            if len(r.read()) > 10:
                return p
            else:
                print "[!] {%s} NONO !" % p
        except:
            print "[!] {%s} NONO !" % p

    def process_item(self, item, spider):

        if 'proxy' in item.keys():
            result = sorted(item['proxy'])
            for line in result:
                lines = self.__proxy(line)
                if lines:
                    rs = lines + "\n"
                    self.file.write(rs)

        return item


class webImgePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return '%s' % image_guid

    def get_media_requests(self, item, info):
        if 'logo_url' in item.keys():
            for url in item['logo_url']:
                if url.count('://') == 1:
                    yield scrapy.Request(url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        # print image_paths
        return item


class webMysqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        print dbargs
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.__insert, item)
        return item

    def __insert(self, tx, item):
        # print item.keys()
        if 'detil_title' in item.keys():
            tx.execute("update spider set introduce ='%s', allprice = '%s' where title = '%s'" % (
                item['introduce'], item['ticket_title'], item['detil_title']))
        if 'title' in item.keys():
            logo_url = [k.strip().split('/')[-1] for k in item['logo_url']]
            allItem = zip(item['title'], logo_url, item['price'], item['saleCount'], item['addressPoint'])
            dd = ["('%s','%s',%s,%s,'%s')" % d for d in allItem]
            tx.execute('insert into spider(title,imgpath,minprice,msales,bdprsion) value%s' % ','.join(dd))

    def __select(self, tx, item):
        pass
