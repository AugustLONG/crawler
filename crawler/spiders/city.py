# -*- coding: utf-8 -*-
import scrapy

from crawler.items.dmoz import DmozItem


class CitySpider(scrapy.Spider):
    name = "city"
    allowed_domains = ["58.com"]
    start_urls = (
        'http://www.58.com/',
    )

    def parse(self, response):
        item = DmozItem()
        sel = scrapy.Selector(response)
        conn = pymssql.connect(host="121.42.136.4", user="sa", password="koala19920716!@#", database="test")
        cursor = conn.cursor()
        sites = sel.xpath("//dl[@id='clist']/dd/a/text()").extract()
        item['title'] = [n.encode('utf-8') for n in sites]
        yield item
        # sql = "select ID,CityName from Cities"
        # cursor.execute(sql)
        # for (ID,CityName) in cursor.fetchall():
        #     print ID
        for name in item['title']:
            # print name
            sql = "Insert into Cities(CityName)values('" + name + "')"
            cursor.execute(sql)
            conn.commit()
