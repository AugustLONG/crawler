#coding: utf-8

import re
import json
from urlparse import urlparse


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


from .log import *


'''
1. 默认取sel.css()[0]，如否则需要'__unique':False or __list:True
2. 默认字典均为css解析，如否则需要'__use':'dump'表明是用于dump数据
'''


class CommonSpider(CrawlSpider):

    ''' # css rule example:
    all_css_rules = {
        '.zm-profile-header': {
            '.zm-profile-header-main': {
                '__use':'dump',
                'name':'.title-section .name::text',
                'sign':'.title-section .bio::text',
                'location':'.location.item::text',
                'business':'.business.item::text',
                'employment':'.employment.item::text',
                'position':'.position.item::text',
                'education':'.education.item::text',
                'education_extra':'.education-extra.item::text',
            }, '.zm-profile-header-operation': {
                '__use':'dump',
                'agree':'.zm-profile-header-user-agree strong::text',
                'thanks':'.zm-profile-header-user-thanks strong::text',
            }, '.profile-navbar': {
                '__use':'dump',
                'asks':'a[href*=asks] .num::text',
                'answers':'a[href*=answers] .num::text',
                'posts':'a[href*=posts] .num::text',
                'collections':'a[href*=collections] .num::text',
                'logs':'a[href*=logs] .num::text',
            },
        }, '.zm-profile-side-following': {
            '__use':'dump',
            'followees':'a.item[href*=followees] strong::text',
            'followers':'a.item[href*=followers] strong::text',
        }
    }
    '''

    # Extract content without any extra spaces.
    # NOTE: If content only has spaces, then it would be ignored.
    def good_content_extract(self, sels):
        contents = []
        for i in sels:
            content = re.sub(r'\s+', ' ', i.extract())
            if content != ' ':
                contents.append(content)
        return contents

    def extract_item(self, sel, rules, item):
        for nk, nv in rules.items():
            if nk in ('__use', '__list'):
                continue
            if nk not in item:
                item[nk] = []
            if sel.css(nv):
                # item[nk] += [i.extract() for i in sel.css(nv)]
                # Without any extra spaces:
                item[nk] += self.good_content_extract(sel.css(nv))
            else:
                item[nk] = []

    def traversal(self, sel, rules, item_class, item, items):
        # print 'traversal:', sel, rules.keys()
        if item is None:
            item = item_class()
        if '__use' in rules:
            if '__list' in rules:
                unique_item = item_class()
                self.extract_item(sel, rules, unique_item)
                items.append(unique_item)
            else:
                self.extract_item(sel, rules, item)
        else:
            for nk, nv in rules.items():
                for i in sel.css(nk):
                    self.traversal(i, nv, item_class, item, items)

    def dfs(self, sel, rules, item_class):
        if sel is None:
            return []
        items = []
        self.traversal(sel, rules, item_class, None, items)
        return items

    def parse_with_rules(self, response, rules, item_class):
        return self.dfs(Selector(response), rules, item_class)

    ''' # use parse_with_rules example:
    def parse_people_with_rules(self, response):
        item = self.parse_with_rules(response, self.all_css_rules, ZhihuPeopleItem)
        item['id'] = urlparse(response.url).path.split('/')[-1]
        info('Parsed '+response.url) # +' to '+str(item))
        return item
    '''
