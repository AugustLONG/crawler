# coding=utf-8
import re
import json

import requests
from scrapy.http import HtmlResponse

response = HtmlResponse(
	url='http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt_Id9NTbaO6ms2zvSBm2RzI&eqs=qBsQoCeguK%2B0ofdI%2B6h3FuvrCqfh1RlwTme4vOefG9aBeZd%2BPz%2FN4dn91sq5UJD2r2xev&ekv=3&page=1')
# response.selector.xpath('//span/text()').extract()
# response.xpath('//title/text()')
# Selector(response=response).xpath('//span/text()').extract()
content = requests.get(response.url).content
# doc=u"""
# <span id="J_realContact" data-real="电话021-60131333 传真021-60131356 &nbsp;&nbsp; <a target='_blank' href='http://my.ctrip.com/uxp/Community/CommunityAdvice.aspx?producttype=3&categoryid=65'>纠错</a>" style="color:#0066cc;cursor:pointer;">联系方式</span>　
# """
# print content
# regex = re.compile(r"sogou\.weixin\.gzhcb\((.*\])\}\)")
# print regex.findall(content)

content = re.search(r'\{.*\]\}', content).group()
docs = ""
for i in json.loads(content)["items"]:
	docs += i
se = HtmlResponse(url="http://www.qq.com", body=docs, encoding="utf8")
print se.xpath("//item//docid/text()").extract()
