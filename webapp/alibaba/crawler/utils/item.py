#coding=utf-8
from django.core.exceptions import ValidationError
from scrapy.item import Field, Item, ItemMeta

class BaseItemMeta(ItemMeta):

    def __new__(mcs, class_name, bases, attrs):
        cls = super(BaseItemMeta, mcs).__new__(mcs, class_name, bases, attrs)
        return cls


class BaseItem(Item):

    __metaclass__ = BaseItemMeta

    unique_key = Field()
    site_name = Field()
    website_id = Field()
    website_name = Field()
    category_name = Field()
    scraper_pk = Field()
    checker_runtime_pk = Field()
    updated = Field()

    def __init__(self, *args, **kwargs):
        super(BaseItem, self).__init__(*args, **kwargs)
        self._instance = None
        self._errors = None

    def save(self, commit=True):
        # if commit:
        #     self.instance.save()
        return self.instance

    @property
    def instance(self):
        if self._instance is None:
            # modelargs = dict((k, self.get(k)) for k in self._values
            #                  if k in self._model_fields)
            self._instance = self.BaseItem(**self._model_fields)
        return self._instance

    def set_fields(self, items_fields):
        # self.fields = self.fields.copy()
        if items_fields:
            for k in items_fields.iterkeys():
                if k not in self.fields:
                    self.fields[k] = Field()