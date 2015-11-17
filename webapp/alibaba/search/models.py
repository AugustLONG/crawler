# coding=utf-8
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from scraper.models import Scraper, Website


class CategoryManager(models.Manager):
    def create(self, name, slug, order=0, **extra_fields):
        """
        Creates and saves a Category with the given name, slug and order.
        """
        if not name:
            raise ValueError('The given name must be set')
        category = self.model(name=name, order=order, slug=slug, **extra_fields)
        category.save()
        return category

    def roots(self):
        categories = self.model.objects.filter(parent__isnull=True, enabled=True)
        return categories

    def chriden(self, pk):
        categories = self.model.objects.filter(parent__pk=pk, enabled=True)
        return categories

    def last_chriden(self, pk):
        categories = self.model.objects.filter(parent__parent__pk=pk, enabled=True)
        return categories


class LinkManager(models.Manager):
    def create(self, name, url, order=0, **extra_fields):
        """
        Creates and saves a Link with the given name, email and password.
        """
        if not name:
            raise ValueError('The given name must be set')
        link = self.model(name=name, order=order, url=url, enabled=True, **extra_fields)
        link.save()
        return link


class TagManager(models.Manager):
    def hot(self):
        categories = self.model.objects.filter(enabled=True).order_by("-hot")
        return categories


class Link(models.Model):
    name = models.CharField(u"名称", max_length=200)
    picture = models.ImageField(u"图片", width_field=100, height_field=100, upload_to='photos', blank=True, null=True)
    url = models.URLField(u"地址")
    enabled = models.BooleanField(u"是否可用", default=True)
    order = models.SmallIntegerField(u"序号", default=0)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)
    objects = LinkManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"友情连接"
        get_latest_by = "created"
        ordering = ("order",)

    # @models.permalink
    def get_absolute_url(self):
        return self.url


class GeneralForms(models.Model):
    FORM_TYPE = (
        ('select', 'SELECT'),
        ('text', 'TEXT'),
        ('datetime', 'DATETIME'),
        ('textarea', 'TEXTAREA'),
        ('date', 'DATE'),
    )
    FORM_VALUE_TYPE = (
        ('char', 'char'),
        ('email', 'email'),
        ('datetime', 'DATETIME'),
        ('ip', 'IP'),
        ('slug', 'SLUG'),
        ('int', 'int'),
        ('date', 'DATE'),
    )
    name = models.CharField(u"简单的说明", max_length=200)
    cname = models.CharField(u"中文", max_length=200, blank=True)
    slug = models.CharField(u"别名", max_length=200, blank=True)
    ename = models.CharField(u"英文", max_length=200, blank=True)
    jname = models.CharField(u"日文", max_length=200, blank=True)
    kname = models.CharField(u"韩文", max_length=200, blank=True)
    rname = models.CharField(u"俄语", max_length=200, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(u"对象ID")
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    form_type = models.CharField(u"表单类型", max_length=10, choices=FORM_TYPE)
    form_value = models.CharField(u"表单值域", max_length=250, help_text=u"如果是表单类型是select,1:v,2:v2", blank=True)
    form_attr = models.CharField(u"表单属性", max_length=250, help_text=u"可以是长度限制，样式调整等", blank=True)
    max_length = models.PositiveIntegerField(u"最大长度", default=200)
    min_length = models.PositiveIntegerField(u"最小长度", default=1)
    value_type = models.CharField(u"值的类型", default="char", max_length=10, choices=FORM_VALUE_TYPE)
    help_text = models.CharField(u"帮助", max_length=250)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"基础表单"

    # @models.permalink
    def get_absolute_url(self):
        return self.pk


class Tag(models.Model):
    name = models.CharField(u"名称", max_length=200)
    slug = models.SlugField(u"别名", max_length=100, db_index=True, unique=True)
    enabled = models.BooleanField(u"是否可用", default=True)
    hot = models.SmallIntegerField(u"热度", default=0)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)
    objects = TagManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"搜索标签"
        get_latest_by = "created"
        ordering = ("hot",)

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'item_detail', None, {'object_id': self.id}


class Category(models.Model):
    name = models.CharField(u"分类名称", max_length=200)
    slug = models.SlugField(u"别名", max_length=100, db_index=True, unique=True)
    parent = models.ForeignKey("self", verbose_name=u"父分类", blank=True, null=True)
    enabled = models.BooleanField(u"是否可用", default=True)
    order = models.SmallIntegerField(u"序号", default=0)
    hot = models.SmallIntegerField(u"热门", default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)
    objects = CategoryManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"搜索分类"
        get_latest_by = "created"
        ordering = ("order",)

    @models.permalink
    def get_absolute_url(self):
        return 'alibaba_search_by_category', None, {'slug': self.slug}

    def chriden(self):
        categories = self.objects.chriden(self.pk)
        return categories

    def last_chriden(self):
        categories = self.objects.last_chriden(self.pk).order_by("-hot")
        return categories


class CategoryForms(models.Model):
    forms = models.ForeignKey(GeneralForms)
    category = models.ForeignKey(Category, blank=True, null=True)
    mustable = models.BooleanField(u"是否必须", default=True)
    nullable = models.BooleanField(u"是否空", default=False)
    searchable = models.BooleanField(u"是否搜索", default=False)
    analyzerable = models.BooleanField(u"是否分词", default=False)
    indexable = models.BooleanField(u"是否索引", default=True)
    default_value = models.CharField(u"默认值", max_length=250)
    htmlable = models.BooleanField(u"允许HTML", default=True)
    order = models.SmallIntegerField(u"排序", default=0)
    editable = models.BooleanField(u"是否可以编辑", default=False)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"分类表单"

    # @models.permalink
    def get_absolute_url(self):
        return self.slug


class PageModule(models.Model):
    CHECKER_TYPE = (
        ('L', 'LIST'),
        ('D', 'DETAIL'),
        ('I', 'INDEX'),
    )
    name = models.CharField(u"名称", max_length=200, blank=True)
    title = models.CharField(u"页面标题", max_length=200, blank=True)
    keywords = models.CharField(u"关键词", max_length=200, blank=True)
    description = models.CharField(u"页面描述", max_length=200, blank=True)
    slug = models.SlugField(u"别名")
    scraper = models.ForeignKey(Scraper)
    category = models.ForeignKey(Category, blank=True, null=True)
    style = models.CharField(u"CSS样式地址", max_length=200)
    js = models.CharField(u"js地址", max_length=200)
    page_type = models.CharField(max_length=1, choices=CHECKER_TYPE, default='L')
    template = models.TextField(u"模板", help_text=u"可以是地址或者内容")
    filter = models.TextField(u"查询和显示条件", help_text=u"地区、分类、tag、网站等组合查询或者显示")
    enabled = models.BooleanField(u"是否可用", default=True)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"页面模块"
        get_latest_by = "created"

    # @models.permalink
    def get_absolute_url(self):
        return self.slug

    def js_path(self):
        return self.js.split(",")

    def style_path(self):
        return self.style.split(",")


class Topic(models.Model):
    name = models.CharField(u"名称", max_length=200)
    title = models.CharField(u"页面标题", max_length=200)
    keywords = models.CharField(u"关键词", max_length=200)
    description = models.CharField(u"页面描述", max_length=200, blank=True, null=True)
    slug = models.SlugField(u"别名")
    category = models.ForeignKey(Category, blank=True, null=True)
    style = models.CharField(u"CSS样式地址", max_length=200)
    js = models.CharField(u"js地址", max_length=200)
    template = models.TextField(u"模板", blank=True, help_text=u"可以是渲染动态或者静态模板")
    url = models.CharField(u"模板地址", max_length=200, blank=True, help_text=u"如果模板和地址都存在，则地址是独立的，可以直接访问")
    enabled = models.BooleanField(u"是否可用", default=True)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"专题"
