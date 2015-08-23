from crawler.spiders.django_spider import DjangoSpider
from scraper.models import Website, GeneralModel, GeneralItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class GeneralSpider(DjangoSpider):
    
    name = 'general'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(Website, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = GeneralModel
        self.scraped_obj_item_class = GeneralItem
        super(GeneralSpider, self).__init__(self, *args, **kwargs)