# -*- coding: utf-8 -*-
import time
import sys

import scrapy
import MySQLdb
from scrapy.http import Request
from scrapy.selector import Selector

reload(sys)
sys.setdefaultencoding('gbk')


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


class MydomainSpider(scrapy.Spider):
    name = "mydomain"
    download_delay = 1
    allowed_domains = ["blog.csdn.net"]
    start_urls = (
        'http://blog.csdn.net/hot.html',
    )

    def parse(self, response):
        items = []
        sel = Selector(response)
        sites = sel.xpath("//div[@class='page_right']/div[@class='blog_list']").extract()
        for site in sites:
            body = Selector(text=site)
            href = body.xpath("//h1/a/@href").extract()
            desc = body.xpath("//h1/a[@class='category']/text()").extract()
            # print len(desc)
            if (len(desc) == 0):
                str = u'[其他]'
                desc.append(str)
            url = href[len(href) - 1]
            # print len(url)
            # print len(desc)
            # print "------------------------------------------"
            yield Request(url=url, meta={'desc': desc[0].encode('utf-8')}, callback=self.parse_word)

    def parse_word(self, response):
        label = response.meta['desc']
        # print type(label)
        if (len(label) == 0):
            label = u'其他'
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        datetime = time.strftime(ISOTIMEFORMAT, time.localtime())
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='blog', port=3306, charset='utf8')
            cursor = conn.cursor()
            word_sel = Selector(response)
            href = response.url
            title = word_sel.xpath(
                "//div[@id='article_details']/div[@class='article_title']/h1/span[@class='link_title']/a/text()").extract()
            body = word_sel.xpath("//div[@class='details']/div[@class='article_content']").extract()
            # label=word_sel.xpath("//div[@id='article_details']/div[@id='article_content']")
            content = str(title[0].encode('utf-8')).replace(' ', '')
            cursor.execute("select * from word where title =%s", content);
            tf = cursor.fetchall()
            if (len(tf) == 0):
                label = label.replace('[', '').replace(']', '')
                cursor.execute("select * from label_list where label_name = '" + label + "'");
                result = cursor.fetchall()
                # if (len(result) == 0):
                #     # print "null"
                #     insert_sql = "Insert into label_list(label_name) VALUE ('" + label + "')";
                #     label_id = cursor.execute(insert_sql)
                #
                # else:
                #     # print result[0][0]
                #     label_id = result[0][0]
                content = str(title[0].encode('utf-8')).replace(' ', '')
                if (len(content) != 0):
                    sql = "Insert into word(title,datetime,label_id,text) values (%s,%s,%s,%s)"
                    print content.decode('utf-8').encode('gbk')
                # parm = (content, datetime, label_id, body[0].encode('utf-8'))
                # cursor.execute(sql, parm)
                # conn.commit()
                # cursor.close()
                # conn.close()
                else:
                    print href
            else:
                print "is have"
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
