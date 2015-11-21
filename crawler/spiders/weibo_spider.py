#! -*- encoding:utf-8 -*-
import time

from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from crawler.items.dmoz import DmozItem


class WeiboSpider(CrawlSpider):
    name = 'weibo'
    allowed_domains = ['weibo.com', 'sina.com.cn']

    def start_requests(self):
        username = '1009137312@qq.com'
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=miniblog&callback=sinaSSOController.preloginCallBack&user=%s&client=ssologin.js(v1.3.14)&_=%s' % \
              (username, str(time.time()).replace('.', ''))
        print url
        return [Request(url=url, method='get', callback=self.parse_item)]

    def parse_item(self, response):
        print response.body
        hxs = HtmlXPathSelector(response)
        i = DmozItem()
        i['id'] = hxs.select('//input[@id="sid"]/@value').extract()
        i['title'] = hxs.select('//div[@id="name"]').extract()
        i['desc'] = hxs.select('//div[@id="description"]').extract()
        return i
