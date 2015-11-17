# Scrapy settings for scrapy_ctrip project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Mozilla'
BOT_VERSION = '5.0'

SPIDER_MODULES = ['scrapy_ctrip.spiders']
NEWSPIDER_MODULE = 'scrapy_ctrip.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
# More comprehensive list can be found at 
# http://techpatterns.com/forums/about304.html
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
]
DOWNLOADER_MIDDLEWARES = {
    'scrapy_ctrip.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy_ctrip.middlewares.ProxyMiddleware': 410,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    # Disable compression middleware, so the actual HTML pages are cached
}

DOWNLOAD_DELAY = 2

DUPEFILTER = True

COOKIES_ENABLED = False

RANDOMIZE_DOWNLOAD_DELAY = True

SCHEDULER_ORDER = 'BFO'

# DOWNLOADER_MIDDLEWARES = {
#         'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
#         'scrapy_ctrip.rotate_useragent.RotateUserAgentMiddleware' :400
# }

DEFAULT_REQUEST_HEADERS = {'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'ch', }
