#coding=utf-8
from django.core.exceptions import ValidationError
from scrapy.item import Field, Item, ItemMeta

class BaseItem(Item):

    def __init__(self, *args, **kwargs):
        super(BaseItem, self).__init__(*args, **kwargs)

    def set_fields(self, items_fields):
        # self.fields = self.fields.copy()
        if items_fields:
            for k in items_fields.iterkeys():
                if k not in self.fields:
                    self.fields[k] = Field()