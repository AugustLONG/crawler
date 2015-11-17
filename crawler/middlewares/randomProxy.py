# coding:utf8


import random

from scrapy import log
from scrapy.exceptions import NotConfigured


class RandomProxy(object):
    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        if not self.proxy_list:
            raise NotConfigured

        with open(self.proxy_list)  as  f:
            self.pro_list = [d.strip() for d in f.readlines() if d]

        if not self.pro_list:
            raise NotConfigured

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):

        if "cn-proxy.com" in request.url:
            return
        if "kuaidaili.com" in request.url:
            return
        if "proxy-list.org" in request.url:
            return
        if 'vipiu.net' in request.url:
            return
        # else:
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
        proxy_address = random.choice(self.pro_list)
        request.meta['proxy'] = '%s' % proxy_address

    # if proxy_user_pass:
    #    basic_auth = 'Basic ' + base64.encodestring('user001:user001')
    #    request.headers['Proxy-Authorization'] = basic_auth

    def process_exception(self, request, exception, spider):
        # print '----',exception
        # print request.meta['handle_httpstatus_all']
        # print dir(request)
        # if 'proxy' in request.meta.keys():
        proxy = request.meta['proxy']
        log.msg('message:%s,url:(%s),failed proxy <%s>' % (exception.message, request, proxy))

    # print request.url
    # return request
