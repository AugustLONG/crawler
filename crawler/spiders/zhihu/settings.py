# -*- coding:utf-8 -*-

BOT_NAME = 'zhihu'

SPIDER_MODULES = ['zhihu.spiders']
NEWSPIDER_MODULE = 'zhihu.spiders'

LOG_FILE = 'zhihu.log'
LOG_LEVEL = 'INFO'

COOKIES_DEBUG = False
RETRY_ENABLED = False
REDIRECT_ENABLED = False

DEPTH_LIMIT = 0
DEPTH_PRIORITY = 0

CONCURRENT_ITEMS = 1000
CONCURRENT_REQUESTS = 100
# The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single domain.
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 0
CONCURRENT_REQUESTS_PER_SPIDER = 100

DNSCACHE_ENABLED = True

DOWNLOAD_DELAY = 0.5
DOWNLOAD_TIMEOUT = 10

ITEM_PIPELINES = {
	'zhihu.pipelines.MongoDBPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
	'zhihu.misc.middleware.CustomHttpProxyMiddleware': 80,
	# 'zhihu.misc.middleware.CustomUserAgentMiddleware': 81,
}

SCHEDULER_ORDER = 'BFO'

HEADER = {
	"Host": "www.zhihu.com",
	"Connection": "keep-alive",
	"Cache-Control": "max-age=0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
	"Referer": "http://www.zhihu.com/people/raymond-wang",
	"Accept-Encoding": "gzip,deflate,sdch",
	"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2",
}

COOKIES = {
	'checkcode': r'"$2a$10$9FVE.1nXJKq/F.nH62OhCevrCqs4skby2bC4IO6VPJITlc7Sh.NZa"',
	'c_c': r'a153f80493f411e3801452540a3121f7',
	'_ga': r'GA1.2.1063404131.1384259893',
	'zata': r'zhihu.com.021715f934634a988abbd3f1f7f31f37.470330',
	'q_c1': r'59c45c60a48d4a5f9a12a52028a9aee7|1400081868000|1400081868000',
	'_xsrf': r'2a7cf7208bf24dbda3f70d953e948135',
	'q_c0': r'"NmE0NzBjZTdmZGI4Yzg3ZWE0NjhkNjkwZGNiZTNiN2F8V2FhRTQ1QklrRjNjNGhMdQ==|1400082425|a801fc83ab07cb92236a75c87de58dcf3fa15cff"',
	'__utma': r'51854390.1063404131.1384259893.1400518549.1400522270.5',
	'__utmb': r'51854390.4.10.1400522270',
	'__utmc': r'51854390',
	'__utmz': r'51854390.1400513283.3.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/hallson',
	'__utmv': r'51854390.100-1|2=registration_date=20121016=1^3=entry_date=20121016=1'
}
