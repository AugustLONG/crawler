# coding=utf-8

from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import Spider
from crawler.items.yeean import YeeyanItem


class YeeyanSpiderSpider(Spider):
    name = 'yeeyan_spider'
    allowed_domains = ['yeeyan.org']
    start_urls = ["http://article.yeeyan.org/list_a"]
    count = 0

    def parse(self, response):
        self.log("OK,%s" % response.url)
        hxs = HtmlXPathSelector(response)
        # 将文章的链接继续进行处理
        divs = hxs.x('//div[@class="publicLeftCon mt10"]')
        for div in divs:
            url = div.x('h5/a/@href').extract()[0]
            yield self.make_requests_from_url(url).replace(callback=self.parse_content)
        # 将下一页的链接继续进行处理
        try:
            next_url = \
            hxs.x('//div[@id="project_left"]/div[@class="publicMiddleLine"]/span/a[b="下一页"]/@href').extract()[0]
        except Exception:
            return
        next_url = 'http://article.yeeyan.org' + next_url
        #  if self.count==10:
        #      return
        #  self.count+=1
        yield self.make_requests_from_url(next_url).replace(callback=self.parse)

    # 过滤文章内容
    def parse_content(self, response):
        hxs = HtmlXPathSelector(response)
        item = YeeyanItem()
        if hxs.x('//a[@class="jx_logo"]/text()'):
            item = self.parse_jx(item, response)
        else:
            item['url'] = response.url
            item['title'] = hxs.x('//title/text()').extract()[0].split('|')[1].strip()
            div = hxs.x('//div[@class="user_info"]')
            item['author'] = div.x('.//h2/a/text()').extract()[0]
            item['excerpt'] = hxs.x('//p[@class="excerpt"]/text()').extract()
            if item['excerpt']:
                item['excerpt'] = item['excerpt'][0]
            else:
                item['excerpt'] = ''
            item['content_html'] = hxs.x('//div[@id="conBox"]').extract()[0]
            item['release_time'] = div.x('.//p/text()').extract()[0].strip()[1:-7]
            item['category'] = hxs.x('//div[@class="crumb"]/a/text()').extract()[1]
        return item

    # 过滤精选的文章
    def parse_jx(self, item, response):
        hxs = HtmlXPathSelector(response)
        item['url'] = response.url
        item['title'] = hxs.x('//title/text()').extract()[0].split('|')[1].strip()
        div = hxs.x('//div[@class="jxar_author"]')
        item['author'] = div.x('.//a/text()').extract()[0]
        item['release_time'] = hxs.x('//p[@class="jxa_info"]/span[1]/text()').extract()[0]
        try:
            item['excerpt'] = hxs.x('//p[@class="jxa_intro"]/text()').extract()[0]
        except Exception:
            item['excerpt'] = None
        item['category'] = hxs.x('//p[@class="jxa_map"]/text()').extract()[1].split()[1]
        item['content_html'] = hxs.x('//div[@class="jxa_content"]').extract()[0]
        return item
