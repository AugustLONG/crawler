# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class ScrapyCtripPipeline(object):
    def __init__(slef):
        self.file = open('item.json', 'wb', encoding='utf-8')


def process_item(self, item, spider):
    line = json.dumps(dict(item)) + "\n"
    self.file.write(line)
    return item


def spider_closed(self, spider):
    self.file.close()
