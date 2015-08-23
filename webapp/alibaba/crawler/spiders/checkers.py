from django.conf import settings
from crawler.spiders.django_checker import DjangoChecker
from scraper.models import GeneralModel


class GeneralChecker(DjangoChecker):
    
    name = 'general_checker'
    
    def __init__(self, *args, **kwargs):
        self._set_ref_object(GeneralModel, **kwargs)
        self.scraper = self.ref_object.website.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.checker_runtime
        super(GeneralChecker, self).__init__(self, *args, **kwargs)