# coding:utf8

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings

runner = Crawler(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
spider = ['proxy', 'where']
for name in spider:
    d = runner.crawl(name)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
