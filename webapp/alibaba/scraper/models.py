# coding=utf-8
import datetime
import json

from django.db import models
import yaml
from django.db.models import Q
from django.contrib.auth.models import User


class Pipelines(models.Model):
    name = models.CharField(u"名称", max_length=200)
    slug = models.SlugField(u"别名", max_length=100, db_index=True, unique=True)
    enabled = models.BooleanField(u"是否可用", default=True)
    conf = models.TextField(u"配置", help_text=u"yaml格式", default='\
"HOST": 15,\n\
"PORT": 10080,\n')
    comments = models.TextField(u"介绍", blank=True)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"管道"
        get_latest_by = "created"

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'item_detail', None, {'object_id': self.id}


class ScrapedObjClass(models.Model):
    name = models.CharField(max_length=200)
    scraper_scheduler_conf = models.TextField(default='\
"MIN_TIME": 15,\n\
"MAX_TIME": 10080,\n\
"INITIAL_NEXT_ACTION_FACTOR": 10,\n\
"ZERO_ACTIONS_FACTOR_CHANGE": 20,\n\
"FACTOR_CHANGE_FACTOR": 1.3,\n')
    checker_scheduler_conf = models.TextField(default='\
"MIN_TIME": 1440,\n\
"MAX_TIME": 10080,\n\
"INITIAL_NEXT_ACTION_FACTOR": 1,\n\
"ZERO_ACTIONS_FACTOR_CHANGE": 5,\n\
"FACTOR_CHANGE_FACTOR": 1.3,\n')
    comments = models.TextField(blank=True)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"Scraped类型"
        ordering = ['name', ]


class ScrapedObjAttr(models.Model):
    ATTR_TYPE_CHOICES = (
        ('S', 'STANDARD'),
        ('T', 'STANDARD (UPDATE)'),
        ('B', 'BASE'),
        ('U', 'DETAIL_PAGE_URL'),
        ('I', 'IMAGE'),
    )
    name = models.CharField(u"字段", max_length=200)
    title = models.CharField(u"名称", max_length=200, blank=True, null=True)
    obj_class = models.ForeignKey(ScrapedObjClass)
    attr_type = models.CharField(max_length=1, choices=ATTR_TYPE_CHOICES)
    id_field = models.BooleanField(default=False)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name + " (" + self.obj_class.__unicode__() + ")"

    class Meta:
        verbose_name_plural = verbose_name = u"属性"
        ordering = ['name', ]


class Scraper(models.Model):
    STATUS_CHOICES = (
        ('A', 'ACTIVE'),
        ('M', 'MANUAL'),
        ('P', 'PAUSED'),
        ('I', 'INACTIVE'),
    )
    CONTENT_TYPE_CHOICES = (
        ('H', 'HTML'),
        ('X', 'XML'),
        ('J', 'JSON'),
        ('S', 'SCRIPT'),
    )
    REQUEST_TYPE_CHOICES = (
        ('R', 'Request'),
        ('F', 'FormRequest'),
    )
    METHOD_CHOICES = (
        ('GET', 'GET'),
        ('POST', 'POST'),
    )
    PAGINATION_TYPE = (
        ('N', 'NONE'),
        ('R', 'RANGE_FUNCT'),
        ('F', 'FREE_LIST'),
    )
    CHECKER_TYPE = (
        ('N', 'NONE'),
        ('4', '404'),
        ('X', '404_OR_X_PATH'),
    )
    name = models.CharField(u"名称", max_length=200)
    slug = models.URLField(u"别名", max_length=100, db_index=True, unique=True)
    enabled = models.BooleanField(u"是否可用", default=True)
    scraped_obj_class = models.ForeignKey(ScrapedObjClass)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    content_type = models.CharField(max_length=1, choices=CONTENT_TYPE_CHOICES, default='H',
                                    help_text="Data type format for scraped main pages (for JSON use JSONPath instead of XPath)")
    detail_page_content_type = models.CharField(max_length=1, choices=CONTENT_TYPE_CHOICES, default='H',
                                                help_text="Data type format for detail pages and checker (for JSON use JSONPath instead of XPath)")
    render_javascript = models.BooleanField(default=False,
                                            help_text="Render Javascript on pages (ScrapyJS/Splash deployment needed, careful: resource intense)")
    max_items_read = models.IntegerField(blank=True, null=True,
                                         help_text="Max number of items to be read (empty: unlimited).")
    max_items_save = models.IntegerField(blank=True, null=True,
                                         help_text="Max number of items to be saved (empty: unlimited).")
    request_type = models.CharField(max_length=1, choices=REQUEST_TYPE_CHOICES, default='R',
                                    help_text="Normal (typically GET) request (default) or form request (typically POST), using Scrapys corresponding request classes (not used for checker).")
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='GET',
                              help_text="HTTP request via GET or POST.")
    headers = models.TextField(blank=True,
                               help_text='Optional HTTP headers sent with each request, provided as a JSON dict (e.g. {"Referer":"http://referer_url"}, use double quotes!)), can use {page} placeholder of pagination.')
    body = models.TextField(blank=True,
                            help_text="Optional HTTP message body provided as a unicode string, can use {page} placeholder of pagination.")
    cookies = models.TextField(blank=True,
                               help_text="Optional cookies as JSON dict (use double quotes!), can use {page} placeholder of pagination.")
    meta = models.TextField(blank=True,
                            help_text="Optional Scrapy meta attributes as JSON dict (use double quotes!), see Scrapy docs for reference.")
    form_data = models.TextField(blank=True,
                                 help_text="Optional HTML form data as JSON dict (use double quotes!), only used with FormRequest request type, can use {page} placeholder of pagination.")
    dont_filter = models.BooleanField(default=False,
                                      help_text="Do not filter duplicate requests, useful for some scenarios with requests falsely marked as being duplicate (e.g. uniform URL + pagination by HTTP header).")
    pagination_type = models.CharField(max_length=1, choices=PAGINATION_TYPE, default='N')
    pagination_on_start = models.BooleanField(default=False)
    pagination_append_str = models.CharField(max_length=200, blank=True,
                                             help_text="Syntax: /somepartofurl/{page}/moreurlstuff.html")
    pagination_page_replace = models.TextField(blank=True,
                                               help_text="RANGE_FUNCT: uses Python range funct., syntax: [start], stop[, step], FREE_LIST: 'Replace text 1', 'Some other text 2', 'Maybe a number 3', ...")
    page_url_script = models.TextField(blank=True, verbose_name=u"列表页执行脚本")
    checker_type = models.CharField(max_length=1, choices=CHECKER_TYPE, default='N')
    checker_x_path = models.CharField(max_length=200, blank=True)
    checker_x_path_result = models.CharField(max_length=200, blank=True)
    checker_ref_url = models.URLField(max_length=500, blank=True)
    comments = models.TextField(blank=True)
    pipelines = models.ManyToManyField(Pipelines, blank=True)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def get_base_elems(self):
        return self.scraperelem_set.filter(scraped_obj_attr__attr_type='B')

    def get_base_elem(self):
        return self.scraperelem_set.get(scraped_obj_attr__attr_type='B')

    def get_detail_page_url_elems(self):
        return self.scraperelem_set.filter(scraped_obj_attr__attr_type='U')

    def get_standard_elems(self):
        q1 = Q(scraped_obj_attr__attr_type='S')
        q2 = Q(scraped_obj_attr__attr_type='T')
        return self.scraperelem_set.filter(q1 | q2)

    def get_id_field_elems(self):
        q1 = Q(scraped_obj_attr__id_field=True)
        return self.scraperelem_set.filter(q1)

    def get_standard_fixed_elems(self):
        return self.scraperelem_set.filter(scraped_obj_attr__attr_type='S')

    def get_standard_update_elems(self):
        return self.scraperelem_set.filter(scraped_obj_attr__attr_type='T')

    def get_standard_update_elems_from_detail_page(self):
        return self.scraperelem_set.filter(scraped_obj_attr__attr_type='T').filter(from_detail_page=True)

    def get_image_elems(self):
        return self.scraperelem_set.filter(scraped_obj_attr__attr_type='I')

    def get_image_elem(self):
        return self.scraperelem_set.get(scraped_obj_attr__attr_type='I')

    def get_scrape_elems(self):
        q1 = Q(scraped_obj_attr__attr_type='S')
        q2 = Q(scraped_obj_attr__attr_type='T')
        q3 = Q(scraped_obj_attr__attr_type='U')
        q4 = Q(scraped_obj_attr__attr_type='I')
        return self.scraperelem_set.filter(q1 | q2 | q3 | q4)

    def get_mandatory_scrape_elems(self):
        q1 = Q(scraped_obj_attr__attr_type='S')
        q2 = Q(scraped_obj_attr__attr_type='T')
        q3 = Q(scraped_obj_attr__attr_type='U')
        q4 = Q(scraped_obj_attr__attr_type='I')
        return self.scraperelem_set.filter(q1 | q2 | q3 | q4).filter(mandatory=True)

    def get_from_detail_page_scrape_elems(self):
        q1 = Q(from_detail_page=True)
        return self.scraperelem_set.filter(q1)

    def __unicode__(self):
        return self.name + " (" + self.scraped_obj_class.name + ")"

    class Meta:
        verbose_name_plural = verbose_name = u"采集器"
        ordering = ['name', 'scraped_obj_class', ]


class ScraperElem(models.Model):
    scraped_obj_attr = models.ForeignKey(ScrapedObjAttr)
    scraper = models.ForeignKey(Scraper)
    x_path = models.CharField(max_length=200)
    reg_exp = models.CharField(max_length=200, blank=True)
    from_detail_page = models.BooleanField(default=False)
    processors = models.CharField(max_length=200, blank=True)
    proc_ctxt = models.TextField(blank=True)
    mandatory = models.BooleanField(default=True)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = verbose_name = u"规则"


class SchedulerRuntime(models.Model):
    TYPE = (
        ('S', 'SCRAPER'),
        ('C', 'CHECKER'),
    )
    runtime_type = models.CharField(max_length=1, choices=TYPE, default='P')
    next_action_time = models.DateTimeField(default=datetime.datetime.now)
    next_action_factor = models.FloatField(blank=True, null=True)
    num_zero_actions = models.IntegerField(default=0)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return unicode(self.id)

    class Meta:
        verbose_name_plural = verbose_name = u"运行状态"
        ordering = ['next_action_time', ]


class Category(models.Model):
    name = models.CharField(u"分类名称", max_length=200)
    slug = models.SlugField(u"别名", max_length=100, db_index=True, unique=True)
    parent = models.ForeignKey("self", verbose_name=u"父分类", blank=True, null=True)
    enabled = models.BooleanField(u"是否可用", default=True)
    order = models.SmallIntegerField(u"序号", default=0)
    hot = models.SmallIntegerField(u"热门", default=0)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"分类"
        get_latest_by = "created"
        ordering = ("order",)


class Sites(models.Model):
    name = models.CharField(u"名称", max_length=200)
    category = models.ForeignKey(Category, verbose_name=u"分类")
    domain = models.CharField(u"域名", max_length=100, db_index=True, unique=True)
    slug = models.SlugField(u"别名", max_length=100, db_index=True, unique=True)
    enabled = models.BooleanField(u"是否可用", default=True)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"站点"
        get_latest_by = "created"

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'item_detail', None, {'object_id': self.id}


class Website(models.Model):
    name = models.CharField(u"名称", max_length=200)
    url = models.URLField(u"地址", db_index=True, unique=True)
    allow_domain = models.CharField(u"允许域名", max_length=200)
    category = models.ForeignKey(Category, verbose_name=u"分类", blank=True, default=True)
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    enabled = models.BooleanField(u"是否可用", default=True)
    site = models.ForeignKey(Sites, verbose_name=u"站点")
    comments = models.TextField(u"介绍", blank=True)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"网址"
        get_latest_by = "created"

    def items_list(self):
        # self.items = json.dumps({"title":u"标题",
        #                          "description":u"描述",
        #                          "url":u"地址",
        #                          "thumbnail":u"图片",
        #                          "website": u"",
        #                          "checker_runtime": u""
        #                          })
        # return json.loads(self.items)
        attrs = self.scraper.scraped_obj_class.scrapedobjattr_set.all()
        items = {}
        for attr in attrs:
            items[attr.name] = attr.title
        return items

    def mongodb_collection(self):
        return self.site.slug + "_" + self.category.slug


class LogMarker(models.Model):
    TYPE_CHOICES = (
        ('PE', 'Planned Error'),
        ('DD', 'Dirty Data'),
        ('IM', 'Important'),
        ('IG', 'Ignore'),
        ('MI', 'Miscellaneous'),
        ('CU', 'Custom'),
    )
    message_contains = models.CharField(max_length=255)
    help_text = "Use the string format from the log messages"
    ref_object = models.CharField(max_length=200, blank=True)
    help_text = 'Choose "Custom" and enter your own type in the next field for a custom type'
    mark_with_type = models.CharField(max_length=2, choices=TYPE_CHOICES, help_text=help_text)
    custom_type = models.CharField(max_length=25, blank=True)
    spider_name = models.CharField(max_length=200, blank=True)
    scraper = models.ForeignKey(Scraper, blank=True, null=True)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = verbose_name = u"日志特性"


class Log(models.Model):
    LEVEL_CHOICES = (
        (50, 'CRITICAL'),
        (40, 'ERROR'),
        (30, 'WARNING'),
        (20, 'INFO'),
        (10, 'DEBUG'),
    )
    message = models.CharField(max_length=255)
    ref_object = models.CharField(max_length=200)
    type = models.CharField(max_length=25, blank=True)
    level = models.IntegerField(choices=LEVEL_CHOICES)
    spider_name = models.CharField(max_length=200)
    scraper = models.ForeignKey(Scraper, blank=True, null=True)
    date = models.DateTimeField(default=datetime.datetime.now)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    @staticmethod
    def numeric_level(level):
        numeric_level = 0
        for choice in Log.LEVEL_CHOICES:
            if choice[1] == level:
                numeric_level = choice[0]
        return numeric_level

    class Meta:
        verbose_name_plural = verbose_name = u"日志"
        ordering = ['-date']
