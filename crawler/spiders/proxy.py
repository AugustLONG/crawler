# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request


class ProxySpider(scrapy.Spider):
    name = "proxy"
    allowed_domains = ["cn-proxy.com", "kuaidaili.com", "proxy-list.org", "vipiu.net", "xrory.com", "ipcn.com"]
    start_urls = (
        'http://www.cn-proxy.com/',
        'http://www.kuaidaili.com/proxylist/1/'
        'http://proxy-list.org/english/index.php?p=1',
        'http://vipiu.net/free/mianfeidaili/2014/04/27/42417.html',
        'http://www.xroxy.com/proxylist.htm',
        'http://proxy.ipcn.org/proxylist.html',
    )

    def parse(self, response):

        if 'kuaidaili.com' in response.url:
            for d in range(1, 11):
                new_url = "http://www.kuaidaili.com/proxylist/%d/" % d
                yield Request(url=new_url, callback=self.fllow_parse)

        if 'cn-proxy.com' in response.url:
            yield Request(url='http://www.cn-proxy.com/', callback=self.fllow_parse)

        if 'proxy-list.org' in response.url:
            for i in range(1, 11):
                pa_url = "http://proxy-list.org/english/index.php?p=%d" % i
                yield Request(url=pa_url, callback=self.fllow_parse)

        if "vipiu.net" in response.url:
            for n in range(2, 5):
                if n == 1:
                    url_v = "http://vipiu.net/free/mianfeidaili/2014/04/27/42417.html"
                else:
                    url_v = "http://vipiu.net/free/mianfeidaili/2014/04/27/42417_%d.html" % n
                yield Request(url=url_v, callback=self.fllow_parse)

    def fllow_parse(self, response):
        item = webProxy()
        if 'kuaidaili.com' in response.url:
            res_k = Selector(response)
            # page = res.xpath('//div[@id = "listnav"]/ul/li[position()>2]/a/@href').extract()
            kui_table = res_k.xpath(
                '//table[@class = "table table-bordered table-striped"]/tbody/tr/td/text()').extract()
            lens = len(kui_table) - 1
            ip = kui_table[0:lens:7]
            port = kui_table[1:lens:7]
            ip_port = [':'.join(k) for k in zip(ip, port)]
            item['proxy'] = ip_port

        if 'cn-proxy.com' in response.url:
            res_c = Selector(response)
            cn_table = res_c.xpath('//table[@class="sortable"]/tbody/tr/td[position()<3]/text()').extract()
            clens = len(cn_table) - 1
            ips = cn_table[0:clens:2]
            ports = cn_table[1:clens:2]
            ip_ports = [':'.join(d) for d in zip(ips, ports)]
            item['proxy'] = ip_ports

        if 'proxy-list.org' in response.url:
            res_p = Selector(response)
            # pages = res.xpath('//div[@class="table-menu"]/a[position()>1]/@href').extract()
            pa_table = res_p.xpath('//div[@class = "table"]/ul/li[position()<3]').extract()
            lens = len(pa_table)
            ips = pa_table[0:lens:2]
            ipget = []
            pare = re.compile('<li class="proxy">(.+)</li>')
            for ip_ in ips:
                ipget.append(re.search(pare, ip_).group(1))
            item['proxy'] = ipget

        if "vipiu.net" in response.url:
            if "_" not in response.url:
                res_v = Selector(response)
                v_table = res_v.xpath('//div[@id="gallery"]/div/text()').extract()
                data = [k.split('@')[0].strip('\r\n\t') for k in v_table]
                item['proxy'] = data
            else:
                res__ = Selector(response)
                v3_table = res__.xpath('//div[@class="wzbody"]/div[position()>2]/text()').extract()
                datas = [k.split('@')[0].strip('\r\n\t') for k in v3_table]
                # print datas
                item['proxy'] = datas

        yield item

    def parse_xproxy(self, response):
        table = response.xpath('/html/body/div[1]/div[2]/table[1]')
        self.log(table)
        for tr in table:
            item = SrcItem()
            item['ip'] = tr.xpath('//table/tr/td[2]/a/text()').extract()
            yield item

    def parse_ipcny(self, response):
        proxylist = response.xpath('//pre/text()').extract()
        self.log(table)
        for proxy in proxylist.split("\n"):
            item = SrcItem()
            yield item


