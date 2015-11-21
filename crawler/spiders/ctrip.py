import json

from scrapy.spiders import Spider
from scrapy.selector import Selector

from crawler.items.ctrip import hotelReview


class ctripSpider(Spider):
    name = 'ctrip'
    allowed_domains = 'http://www.ctrip.com/'
    start_urls = ['http://hotels.ctrip.com/hotel/dianping/441507_p1t0.html']

    # callback function when received response
    def parse(self, response):
        sel = Selector(response)
        item = hotelReview()
        aspect_rate = sel.xpath(".//*[@class='comment_detail']/text()").extract()
        print str(response.body).decode('GB2312').encode('utf8')

        filename = response.url.split('/')[-1].split('_')[0]
        item['content'] = json.dumps(aspect_rate, ensure_ascii=False).encode('utf8')
        print item
        with open(filename, 'a') as file:
            content = str(item['content'])
            file.write(content)
