# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import sys, os, random

reload(sys)
sys.setdefaultencoding('utf-8')

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE = os.path.join(PROJECT_ROOT, '../static/upload/thumbnails')

BOT_NAME = 'crawler'

# A list of modules where Scrapy will look for spiders.
SPIDER_MODULES = ['crawler.spiders']
# Module where to create new spiders using the genspider command.
NEWSPIDER_MODULE = 'crawler.spiders'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16
# Maximum number of concurrent items (per response) to process in parallel in the Item Processor
CONCURRENT_ITEMS = 100

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN=16
# CONCURRENT_REQUESTS_PER_IP=16

# The maximum depth that will be allowed to crawl for any site. If zero, no limit will be imposed.
DEPTH_LIMIT = 0
# An integer that is used to adjust the request priority based on its depth.If zero, no priority adjustment is made from depth.
DEPTH_PRIORITY = 0
# Whether to collect maximum depth stats.
DEPTH_STATS = True
# Whether to collect verbose depth stats. If this is enabled, the number of requests for each depth is collected in the stats.
DEPTH_STATS_VERBOSE = False

# Whether to enable DNS in-memory cache.
DNSCACHE_ENABLED = True
# DNS in-memory cache size.
DNSCACHE_SIZE = 10000
# Timeout for processing of DNS queries in seconds. Float is supported.
DNS_TIMEOUT = 60

# Disable cookies (enabled by default)
# COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
    # 'scrapy.extensions.corestats.CoreStats': 0,
    # 'scrapy.telnet.TelnetConsole': 0,
    # 'scrapy.extensions.memusage.MemoryUsage': 0,
    # 'scrapy.extensions.memdebug.MemoryDebugger': 0,
    # 'scrapy.extensions.closespider.CloseSpider': 0,
    # 'scrapy.extensions.feedexport.FeedExporter': 0,
    # 'scrapy.extensions.logstats.LogStats': 0,
    # 'scrapy.extensions.spiderstate.SpiderState': 0,
    # 'scrapy.extensions.throttle.AutoThrottle': 0,
    'scrapy.telnet.TelnetConsole': None,
}

# A boolean which specifies if the telnet console will be enabled (provided its extension is also enabled).
TELNETCONSOLE_ENABLED = True
# The port range to use for the telnet console. If set to None or 0, a dynamically assigned port is used. For more info see Telnet Console.
#  http://doc.scrapy.org/en/latest/topics/telnetconsole.html#topics-telnetconsole
TELNETCONSOLE_PORT = [6023, 6073]

# Dump the Scrapy stats (to the Scrapy log) once the spider finishes.
# http://doc.scrapy.org/en/latest/topics/stats.html#topics-stats
STATS_DUMP = True
# The class to use for collecting stats, who must implement theS tats Collector API
# http://doc.scrapy.org/en/latest/topics/api.html#topics-api-stats
# STATS_CLASS="scrapy.statscollectors.MemoryStatsCollector'"
# Send Scrapy stats after spiders finish scraping. See StatsMailer for more info.
# STATSMAILER_RCPTS=[]

# The maximum URL length to allow for crawled URLs. For more information about the default value for this setting see: http://www.boutell.com/newfaq/misc/urllength.html
# URLLENGTH_LIMIT=2083


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
# AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
# 'crawler.pipelines.AlibabaImagesPipeline': 200,
# 'crawler.pipelines.ValidationPipeline': 400,
# 'crawler.pipelines.AlibabaMongoDBPipeline': 800,
# 'crawler.pipelines.mongo.MongoPipeline': 900,
# }

# DSCRAPER_IMAGES_STORE_FORMAT = 'ALL'
#
# DSCRAPER_LOG_ENABLED = True
# DSCRAPER_LOG_LEVEL = 'INFO'
# DSCRAPER_LOG_LIMIT = 5

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
# 'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
# 'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
# 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
# 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
# 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
# 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
# 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
# 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
# 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
# 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
# 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
# 'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware': 830,
# 'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
# 'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
# 'crawler.middlewares.useragent.RandomUserAgent': 1,  # 随机user agent
# 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110, #代理需要用到
# 'crawler.middlewares.ProxyMiddleware': 100, #代理需要用到
# 'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware' : None,
# 'crawler.middlewares.redis_retry.RedisRetryMiddleware': 510,
# }
DOWNLOAD_HANDLERS = {
    # 'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
    # 'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    # 'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    # 's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
}

RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408]
DOWNLOAD_TIMEOUT = 20
DOWNLOAD_DELAY = 10
DOWNLOAD_WARNSIZE = 0  # The response size (in bytes) that downloader will start to warn.
DOWNLOAD_MAXSIZE = 0

# The class used to detect and filter duplicate requests.
# DUPEFILTER_CLASS = "crawler.utils.bloomfilter.BLOOMDupeFilter"
# DUPEFILTER_DEBUG=False

SETTINGS_PRIORITIES = {
    'default': 0,
    'command': 10,
    'project': 20,
    'spider': 30,
    'cmdline': 40,
}
# Don't cleanup redis queues, allows to pause/resume crawls.
# SCHEDULER_PERSIST = True
SCHEDULER = 'scrapy.core.scheduler.Scheduler'
# A dict containing the scrapy contracts enabled in your project, used for testing spiders
# SPIDER_CONTRACTS={
#     'scrapy.contracts.default.UrlContract' : 1,
#     'scrapy.contracts.default.ReturnsContract': 2,
#     'scrapy.contracts.default.ScrapesContract': 3,
# }
# The class that will be used for loading spiders,
# SPIDER_LOADER_CLASS="'scrapy.spiderloader.SpiderLoader'"
# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'crawler.middlewares.MyCustomSpiderMiddleware': 543,
#    'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': None,
#     'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
#     'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
#     'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
#     'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
#     'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
# }

# how long we want the duplicate timeout queues to stick around in seconds
# DUPEFILTER_TIMEOUT = 60

# how many times to retry getting an item from the queue before the spider is considered idle
# SCHEUDLER_ITEM_RETRIES = 3

LOG_LEVEL = 'INFO'  # CRITICAL, ERROR, WARNING, INFO, DEBUG
# Disable the built in logging in production
LOG_ENABLED = True
# If True, all standard output (and error) of your process will be redirected to the log. For example if you print 'hello' it will appear in the Scrapy log.
LOG_STDOUT = False
# LOG_ENCODING="utf-8'"
# LOG_FILE = "/var/log/scrapy.log"
# LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
# LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# Allow all return codes
# HTTPERROR_ALLOW_ALL = True

# Whether to enable memory debugging.
MEMDEBUG_ENABLED = False
# When memory debugging is enabled a memory report will be sent to the specified addresses if this setting is not empty, otherwise the report will be written to the log.
MEMDEBUG_NOTIFY = ['admin@yueguangba.com']
# Whether to enable the memory usage extension that will shutdown the Scrapy process when it exceeds a memory limit, and also notify by email when that happened.
MEMUSAGE_ENABLED = False
# The maximum amount of memory to allow (in megabytes) before shutting down Scrapy (if MEMUSAGE_ENABLED is True). If zero, no check will be performed.
MEMUSAGE_LIMIT_MB = 0
# A list of emails to notify if the memory limit has been reached.
MEMUSAGE_NOTIFY_MAIL = ['admin@yueguangba.com']
# Whether to send a memory usage report after each spider has been closed.
MEMUSAGE_REPORT = False
# The maximum amount of memory to allow (in megabytes) before sending a warning email notifying about it. If zero, no warning will be produced.
MEMUSAGE_WARNING_MB = 0

# Whether the Redirect middleware will be enabled.
REDIRECT_ENABLED = True
# The maximum number of redirections that will be follow for a single request.
REDIRECT_MAX_TIMES = 1
# Whether the Meta Refresh middleware will be enabled.
METAREFRESH_ENABLED = True
# The maximum meta-refresh delay (in seconds) to follow the redirection.
REDIRECT_MAX_METAREFRESH_DELAY = 100

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    # Chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36 OPR/32.0.1948.69",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36 OPR/32.0.1948.69",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36 OPR/32.0.1948.69",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36 OPR/32.0.1948.69",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36 OPR/32.0.1948.69",

    # Firefox
    "Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0",
    "Mozilla/5.0 (Windows NT 6.3; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",

    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
]

USER_AGENT = random.choice(USER_AGENTS)

# PROXIES = [
#     {'ip_port': '111.11.228.75:80', 'user_pass': ''},
#     {'ip_port': '120.198.243.22:80', 'user_pass': ''},
#     {'ip_port': '111.8.60.9:8123', 'user_pass': ''},
#     {'ip_port': '101.71.27.120:80', 'user_pass': ''},
#     {'ip_port': '122.96.59.104:80', 'user_pass': ''},
#     {'ip_port': '122.224.249.122:8088', 'user_pass': ''},
# ]

# These settings define the default constructor values of the MailSender class,
# and can be used to configure e-mail notifications in your project without writing any code
# (for those extensions and code that uses MailSender).
MAIL_FROM = "crawler@yueguangba.com"
MAIL_HOST = "localhost"
MAIL_PORT = 25
MAIL_USER = "crawler"
MAIL_PASS = "crawler"
MAIL_TLS = False
MAIL_SSL = False

REDIS_UNIQUE_KEY = "alibaba.crawler.item.unique_key"

LOCAL_HOST = "127.0.0.1"
MONGO_HOST = LOCAL_HOST
MONGODB_URI = "mongodb://" + MONGO_HOST + ":27017"
MONGODB_DATABASE = 'alibaba'
MONGODB_COLLECTION = 'items'
MONGODB_ADD_TIMESTAMP = True
MONGODB_UNIQUE_KEY = "url"
# MONGODB_BUFFER_DATA = 10
# MONGODB_REPLICA_SET = 'myReplicaSetName'
# MONGODB_URI = 'mongodb://host1.example.com:27017,host2.example.com:27017,host3.example.com:27017'

ELASTICSEARCH_SERVER = '127.0.0.1'  # If not 'localhost' prepend 'http://'
ELASTICSEARCH_PORT = 9200  # If port 80 leave blank
ELASTICSEARCH_USERNAME = ''
ELASTICSEARCH_PASSWORD = ''
ELASTICSEARCH_INDEX = 'scrapy'
ELASTICSEARCH_TYPE = 'items'
ELASTICSEARCH_UNIQ_KEY = 'url'

# A boolean which specifies if the web service will be enabled (provided its extension is also enabled).
JSONRPC_ENABLED = True
# A file to use for logging HTTP requests made to the web service. If unset web the log is sent to standard scrapy log.
JSONRPC_LOGFILE = None
# The interface the web service should listen on.
JSONRPC_HOST = '127.0.0.1'
# The port range to use for the web service. If set to None or 0, a dynamically assigned port is used.
JSONRPC_PORT = [6080, 7030]

# Kafka server information
KAFKA_HOSTS = ''
KAFKA_TOPIC_PREFIX = 'demo'

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
PROXY_LIST = os.path.join(PROJECT_ROOT, 'proxy.txt')

IMAGES_THUMBS = {
    'medium': (200, 200),
    'small': (100, 100),
}

try:
    from local_settings import *
except:
    pass
