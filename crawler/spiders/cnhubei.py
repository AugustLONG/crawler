# -*- coding: utf-8 -*-
import time
import sys

import scrapy
from scrapy.selector import Selector

from crawler.items.dmoz import DmozItem

reload(sys)
sys.setdefaultencoding('utf8')


class CnhubeiSpider(scrapy.Spider):
    name = "cnhubei"
    allowed_domains = ["cnhubei.com"]
    start_urls = [
        "http://news.cnhubei.com"
    ]

    def parse(self, response):
        items = []
        sel = Selector(response)
        sites = sel.xpath("//div[@class='first_box_mid left']/div[@class='news_mid_box']").extract()
        for site in sites:
            body = Selector(text=site)
            desc = body.xpath("//div[@class='news_subnav_2']/h1/text()").extract()
            for list in body.xpath("//ul/li").extract():
                item = DmozItem()
                list_body = Selector(text=list)
                links = list_body.xpath("//a/@href").extract()
                if (links[0][0] == "."):
                    links[0] = "http://news.cnhubei.com" + links[0][1:]
                # print links[0]
                # print type(links[0])
                # print "--------------"
                yield scrapy.Request(url=links[0], meta={'desc': desc[0].encode('utf-8'), 'source': response.url},
                                     callback=self.parse_word)

        sites2 = sel.xpath("//div[@class='first_box_mid left']/div[@class='news_mid_box cBlue']").extract()
        for site in sites2:
            body = Selector(text=site)
            desc = body.xpath("//div[@class='news_subnav_2']/h1/text()").extract()
            for list in body.xpath("//ul/li").extract():
                item = DmozItem()
                list_body = Selector(text=list)
                links = list_body.xpath("//a/@href").extract()
                if (links[0][0] == "."):
                    links[0] = "http://news.cnhubei.com" + links[0][1:]
                yield scrapy.Request(url=links[0], meta={'desc': desc[0].encode('utf-8')}, callback=self.parse_word)

    def parse_word(self, response):
        # print response.meta['desc']
        item = DmozItem()
        desc = response.meta['desc']
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        conn = pymssql.connect(host="121.42.136.4", user="sa", password="koala19920716!@#", database="OpenData")
        cursor = conn.cursor()
        word_sel = Selector(response)
        href = response.url
        title = word_sel.xpath("//div[@class='left_content']/div[@class='title']/text()").extract()
        body = word_sel.xpath("//div[@class='left_content']/div[@class='content_box']/p").extract()
        content = ''
        if (len(body) == 0):
            body = word_sel.xpath("//div[@class='left_content']/div[@class='content_box']/div").extract()
        for n in body:
            p_site = Selector(text=n)
            img_src = p_site.xpath("//img/@oldsrc").extract()
            if (len(img_src) != 0):
                url_obj = href.split('/')
                url = ""
                for i in range(0, len(url_obj) - 1):
                    url += url_obj[i] + "/"
                old_str = "./" + str(img_src[0]).encode("utf-8")
                new_str = str(url).encode("utf-8") + str(img_src[0]).encode("utf-8")
                n = n.replace(old_str, new_str)
                content += n
            else:
                content += n
        # item['title']=[n.decode("utf8").encode('gbk') for n in title]
        # item['body']=content.decode("utf8").encode('gbk')
        # item['desc']=desc.decode("utf8").encode('gbk')
        # item['link']=href.decode("utf8").encode('gbk')
        select_sql = "select * from  T_News where title=%s"
        parm = (title[0].encode('utf-8'))
        cursor.execute(select_sql, parm)
        result = cursor.fetchall()
        if (len(result) == 0):
            sql = "Insert into T_News(Title,Content,DateTime,Url,Source,Category)values('" + title[0].encode(
                'utf-8') + "','" + content.encode('utf-8') + "','" + time.strftime(ISOTIMEFORMAT,
                                                                                   time.localtime()) + "','" + href.encode(
                'utf-8') + "','荆楚网','" + desc + "')"
            cursor.execute(sql)
            conn.commit()
        else:
            print "Is have"
