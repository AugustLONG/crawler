from scrapy.item import Item, Field


class DMOZ(Item):
	name = Field()
	description = Field()
	url = Field()
