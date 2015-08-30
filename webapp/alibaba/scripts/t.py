# coding=utf-8
from scrapy import Selector
from scrapy.http import HtmlResponse
# response = HtmlResponse(url='http://example.com')
# response.selector.xpath('//span/text()').extract()
# response.xpath('//title/text()')
# Selector(response=response).xpath('//span/text()').extract()

doc=u"""
<span id="J_realContact" data-real="电话021-60131333 传真021-60131356 &nbsp;&nbsp; <a target='_blank' href='http://my.ctrip.com/uxp/Community/CommunityAdvice.aspx?producttype=3&categoryid=65'>纠错</a>" style="color:#0066cc;cursor:pointer;">联系方式</span>　
"""
sel = Selector(text=doc, type="html")
print sel.xpath('//span[@id="J_realContact"]/@data-real').re(r'\s*(.*)<a')