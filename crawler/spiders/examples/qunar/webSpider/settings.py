# -*- coding: utf-8 -*-

# Scrapy settings for webSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os

TOP_DIR = os.path.dirname(__file__)

if not TOP_DIR:
    TOP_DIR = "."

log_path = os.path.join(TOP_DIR, 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)

IMAGES_STORE = os.path.join(TOP_DIR, 'imgLogo')
if not os.path.exists(IMAGES_STORE):
    os.mkdir(IMAGES_STORE)

BOT_NAME = 'webSpider'

SPIDER_MODULES = ['webSpider.spiders']
NEWSPIDER_MODULE = 'webSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'webSpider (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'scrapy.contrib.pipeline.images.ImagesPipeline': 150,
    'webSpider.pipelines.webImgePipeline': 550,
    'webSpider.pipelines.WebspiderPipeline': 300,
    'webSpider.pipelines.webMysqlPipeline': 455,

}

DEFAULT_REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Accept-Language': 'en',
                           'Accept-Encoding': 'gzip, deflate',
                           }

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    # Fix path to this module
    'webSpider.downMiddler.randomProxy.RandomProxy': 100,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,

}
# DOWNLOAD
# DOWNLOAD_DELAY = 0.5
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_TIMEOUT = 120
# CONCURRENT_REQUESTS_PER_IP = 2

LOG_ENABLED = True
LOG_ENCODING = 'UTF-8'
LOG_FILE = '%s/p.log' % log_path
LOG_LEVEL = 'INFO'
RETRY_ENABLED = True
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
RETRY_TIMES = 10
DUPEFILTER_DEBUG = True
# IMAGES_THUMBS = {
#    'small': (50, 50),
#    'big': (270, 270),
# }

# mysql
'''
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_DBNAME = 'test'
MYSQL_HOST = '180.169.19.187'
MYSQL_PORT = 3306
MYSQL_USER = 'idexadmin'
MYSQL_PASSWD = 'idex000'
MYSQL_DBNAME = 'demo'
'''
MYSQL_HOST = '180.169.19.148'
MYSQL_PORT = 3306
MYSQL_USER = 'idexadmin'
MYSQL_PASSWD = 'idex000'
MYSQL_DBNAME = 'test'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_URL = "redis://@localhost:6379"

COOKIES_ENABLED = False
PROXY_LIST = os.path.join(TOP_DIR, 'proxyList.txt')
f = open(PROXY_LIST, 'a')
f.close()
# scheduler
