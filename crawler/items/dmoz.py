from scrapy.item import Item, Field


class DmozItem(Item):
    name = Field()
    description = Field()
    url = Field()
