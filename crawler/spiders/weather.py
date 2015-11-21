# -*- coding: utf-8 -*-
import json
import time

import scrapy
from scrapy.selector import Selector
from scrapy.http import Request

from crawler.items.dmoz import DmozItem


def change_word(s):
    sum = 0
    for i in s[0]:
        sum += 1
    ss2 = ''

    for i in range(0, sum):
        if (s[0][i] == u'\u2014'):
            continue
        ss2 += s[0][i]

    s = ss2
    print s
    return s


class WeatherSpider(scrapy.Spider):
    name = "weather"
    allowed_domains = ["etouch.cn"]
    start_urls = (
        'http://wthrcdn.etouch.cn/weather_mini?city=北京',
    )
    i = 2

    def parse(self, response):
        items = []
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        item = DmozItem()
        sites = Selector(text=response.body)
        detail_url_list = sites.xpath('//p/text()').extract()
        conn = pymssql.connect(host="121.42.136.4", user="sa", password="koala19920716!@#", database="test")
        cursor = conn.cursor()
        for site in detail_url_list:
            item["json"] = json.loads(site)
            items.append(item)
        for site in items:
            jsons = json.dumps(site["json"]).encode("utf-8")
            ddata = json.loads(jsons)
            if (ddata['desc'] == "OK"):
                for info in ddata['data']['forecast']:
                    sql = "Insert into Weather(city_name,wendu,ganmao,fengxiang,fengli,high,low,weather_type,show_date,datetime)values('" + \
                          ddata['data']['city'].encode('utf-8') + "'," + ddata['data']['wendu'].encode('utf-8') + ",'" + \
                          ddata['data']['ganmao'].encode('utf-8') + "','" + info['fengxiang'].encode('utf-8') + "','" + \
                          info['fengli'].encode('utf-8') + "','" + info['high'].encode('utf-8') + "','" + info[
                              'low'].encode('utf-8') + "','" + info['type'].encode('utf-8') + "','" + info[
                              'date'].encode('utf-8') + "','" + time.strftime(ISOTIMEFORMAT, time.localtime()) + "')"
                    cursor.execute(sql)
                    conn.commit()

        int = WeatherSpider.i - 1
        sql = "select Top 1 CityName from Cities where id not in (select top " + str(int) + " id from Cities)"
        cursor.execute(sql)
        for (CityName) in cursor.fetchall():
            url = "http://wthrcdn.etouch.cn/weather_mini?city=" + change_word(CityName)
            yield Request(url, callback=self.parse)
        WeatherSpider.i += 1
