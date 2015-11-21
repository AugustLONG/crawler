import time
import sys

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import MySQLdb

from crawler.items.dmoz import DmozItem

reload(sys)
sys.setdefaultencoding('utf8')


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


class DmozSpider(scrapy.spiders.Spider):
    name = "dmoz"
    download_delay = 1
    allowed_domains = ["blog.csdn.net"]
    start_urls = [
        "http://blog.csdn.net/u012150179/article/details/11749017"
    ]

    def parse(self, response):
        sel = Selector(response)
        item = DmozItem()
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        datetime = time.strftime(ISOTIMEFORMAT, time.localtime())
        conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='blog', port=3306, charset='utf8')
        cursor = conn.cursor()

        article_url = str(response.url)
        article_name = sel.xpath('//div[@id="article_details"]/div/h1/span/a/text()').extract()
        article_body = sel.xpath('//div[@id="article_details"]/div[@id="article_content"]').extract()
        article_label = sel.xpath('//div[@class="article_manage"]/span[@class="link_categories"]/a/text()').extract()
        if (len(article_label) != 0):
            item['article_label'] = article_label[0].encode('utf-8')
            if (len(article_name[0]) != 0):
                item['article_name'] = article_name[0].encode('utf-8')
                item['article_url'] = article_url.encode('utf-8')
                if (len(article_body) != 0):
                    item['body'] = article_body[0].encode('utf-8')
                    # yield item
                    cursor.execute("select * from label_list where label_name = '" + item['article_label'] + "'");
                    result = cursor.fetchall()
                    if (len(result) == 0):
                        # print "null"
                        insert_sql = "Insert into label_list(label_name) VALUE ('" + item['article_label'] + "')";
                        label_id = cursor.execute(insert_sql)

                    else:
                        # print result[0][0]
                        label_id = result[0][0]

                    sql = "Insert into word(title,datetime,label_id,text) values (%s,%s,%s,%s)"
                    parm = (item['article_name'], datetime, label_id, item['body'])
                    print sql
                # cursor.execute(sql, parm)
                # conn.commit()
                else:
                    print article_url
                    print "body is null"
            else:
                print article_url
                print "title is null"
        else:
            print article_url
            print "label is null"

        urls = sel.xpath('//li[@class="next_article"]/a/@href').extract()
        for url in urls:
            url = "http://blog.csdn.net" + url
            # print type(url)
            yield Request(url, callback=self.parse)
