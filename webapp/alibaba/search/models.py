#coding=utf-8
from django.db import models


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
        ordering = ("hot", )

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
        ordering = ("order", )

    @models.permalink
    def get_absolute_url(self):
        return 'search_by_category', None, {'slug': self.slug}

    def chriden(self):
        categories = self.objects.chriden(self.pk)
        return categories

    def last_chriden(self):
        categories = self.objects.last_chriden(self.pk).order_by("-hot")
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
        ordering = ("order", )

    # @models.permalink
    def get_absolute_url(self):
        return self.url

from scraper.models import Scraper, Website
class PageModule(models.Model):
    CHECKER_TYPE = (
        ('L', 'LIST'),
        ('D', 'DETAIL'),
        ('I', 'INDEX'),
    )
    name = models.CharField(u"页面名称", max_length=200)
    slug = models.SlugField(u"别名")
    scraper = models.ForeignKey(Scraper)
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
        verbose_name_plural = verbose_name = u"友情连接"
        get_latest_by = "created"

    # @models.permalink
    def get_absolute_url(self):
        return self.slug

    def js_path(self):
        return self.js.split(",")

    def style_path(self):
        return self.style.split(",")

