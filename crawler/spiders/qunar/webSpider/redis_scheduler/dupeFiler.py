#coding:utf8

import time
from redis_scheduler import  redisConnect
from scrapy.dupefilter import BaseDupeFilter
from scrapy.utils.request import request_fingerprint


class RFPDupeFilter(BaseDupeFilter):
    def __init__(self,server,key):
        self.server = server
        self.key = key
    
    
    @classmethod
    def from_settings(self,settings):
        server = redisConnect.from_settings(settings)
        
        
   
        
        
