from scrapy import  signals
import logging as log
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from crawler.spiders.django_base_spider import DjangoBaseSpider
from scraper.models import Scraper


class CheckerTest(DjangoBaseSpider):
    
    name = 'checker_test'
    
    command = 'scrapy crawl checker_test -a id=SCRAPER_ID'
    
    def __init__(self, *args, **kwargs):
        self._set_ref_object(Scraper, **kwargs)
        self._set_config(**kwargs)
        
        if self.ref_object.checker_type == 'N':
            msg = "No checker defined for scraper!"
            log.msg(msg, log.ERROR)
            raise CloseSpider(msg)

        idf_elems = self.ref_object.get_id_field_elems()
        if not (len(idf_elems) == 1 and idf_elems[0].scraped_obj_attr.attr_type == 'U'):
            msg = 'Checkers can only be used for scraped object classed defined with a single DETAIL_PAGE_URL type id field!'
            log.msg(msg, log.ERROR)
            raise CloseSpider(msg)
        
        if self.ref_object.checker_type == '4':
            if not self.ref_object.checker_ref_url:
                msg = "Please provide a reference url for your 404 checker (Command: %s)." % (self.command)
                log.msg(msg, log.ERROR)
                raise CloseSpider(msg)
        
        if self.ref_object.checker_type == 'X':
            if not self.ref_object.checker_x_path or not self.ref_object.checker_ref_url:
                msg = "Please provide the necessary x_path fields for your 404_OR_X_PATH checker (Command: %s)." % (self.command)
                log.msg(msg, log.ERROR)
                raise CloseSpider(msg)
        
        self.start_urls.append(self.ref_object.checker_ref_url)
        dispatcher.connect(self.response_received, signal=signals.response_received)
    
    
    def _set_config(self, **kwargs):
        log_msg = ""
        super(CheckerTest, self)._set_config(log_msg, **kwargs)
    
    
    def spider_closed(self):
        pass
    
    
    def start_requests(self):
        for url in self.start_urls:
            meta = {}
            if self.ref_object.detail_page_content_type == 'H' and self.ref_object.render_javascript:
                meta['splash'] = {
                    'endpoint': 'render.html',
                    'args': self.conf['SPLASH_ARGS'].copy()
                }
            yield Request(url, self.parse, meta=meta)


    def response_received(self, **kwargs):
        if kwargs['response'].status == 404:
            if self.ref_object.checker_type == '4':
                self.log("Checker configuration working (ref url request returning 404).", log.INFO)
            if self.ref_object.checker_type == 'X':
                self.log('A request of your ref url is returning 404. Your x_path can not be applied!', log.WARNING)
        else:
            if self.ref_object.checker_type == '4':
                self.log('Ref url request not returning 404!', log.WARNING)
    
    def parse(self, response):        
        if self.ref_object.checker_type == '4':
            return

        try:
            test_select = response.xpath(self.ref_object.checker_x_path).extract()
        except ValueError:
            self.log('Invalid checker x_path!', log.ERROR)
            return
        if len(test_select) == 0:
            self.log("Checker configuration not working (no elements found for xpath on reference url page)!", log.ERROR)
        else:
            if self.ref_object.checker_x_path_result == '':
                self.log("Checker configuration working (elements for x_path found on reference url page (no x_path result defined)).", log.INFO)
            else:
                if test_select[0] != self.ref_object.checker_x_path_result:
                    self.log("Checker configuration not working (expected x_path result not found on reference url page)!", log.ERROR)
                else:
                    self.log("Checker configuration working (expected x_path result found on reference url page).", log.INFO)
                
        