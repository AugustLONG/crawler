#encoding: utf-8
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from misc.store import doubanDB
from parsers import *

class AlbumSpider(CrawlSpider):
    name = "album"
    allowed_domains = ["www.douban.com"]
    start_urls = [
        "http://www.douban.com/",
    ]

    rules = (
        #相册详情
        Rule(LinkExtractor(allow=r"^http://www\.douban\.com/photos/album/\d+/($|\?start=\d+)"),
            callback="parse_album", 
            follow=True
        ),

        #照片详情
        Rule(LinkExtractor(allow=r"^http://www\.douban\.com/photos/photo/\d+/$"),
            callback = "parse_photo",
            follow = True
        ),

        #豆列集合 
        # Rule(LinkExtractor(allow=r"^http://www\.douban\.com/photos/album/\d+/doulists$"),
        #     follow=True
        # ),

        #单个豆列
        Rule(LinkExtractor(allow=r"^http://www\.douban\.com/doulist/\d+/$"),
            follow=True
        ),        
    )

    def parse_album(self, response):
        album_parser = AlbumParser(response)
        item = dict(album_parser.item)
        
        if album_parser.next_page: return None
        spec = dict(from_url = item["from_url"])
        doubanDB.album.update(spec, {"$set": item}, upsert=True)
     
    def parse_photo(self, response):
        single = SinglePhotoParser(response)
        from_url = single.from_url
        if from_url is None: return
        doc = doubanDB.album.find_one({"from_url": from_url}, {"from_url":True})

        item = dict(single.item)
        if not doc: 
            new_item = {}
            new_item["from_url"] = from_url
            new_item["photos"] = item
            doubanDB.album.save(new_item)
        else:
            spec = {"from_url": from_url}
            doc = doubanDB.album.find_one({"photos.large_img_url": item["large_img_url"]})
            if not doc:
                doubanDB.album.update(spec, {"$push": {"photos": item}})
        
        cp = CommentParser(response)
        comments = cp.get_comments()
        if not comments: return
        large_img_url = item["large_img_url"]
        spec = {"photos.large_img_url": large_img_url }
        doubanDB.album.update(spec, {"$set": {"photos.$.comments": comments} }, upsert=True)