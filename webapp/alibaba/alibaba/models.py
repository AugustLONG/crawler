# encoding:utf-8
import datetime
from django.core.urlresolvers import reverse
from django.db import models


class Country(models.Model):
    """
    国家
    """
    name = models.CharField(u'名称', max_length=200, blank=True)
    chart = models.CharField(u'url标志', max_length=200, blank=True)
    ename = models.CharField(u'英文简称', max_length=200, blank=True)
    status = models.BooleanField(u"启用", default=False)
    latitude = models.FloatField(u'经度', max_length=100, default=0.0)
    longitude = models.FloatField(u'纬度', max_length=100, default=0.0)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = verbose_name = u"国家"

    def __unicode__(self):
        return u'%s' % self.name

    # def get_absolute_url(self):
    #     return reverse('country_index', kwargs={'country_chart': self.chart})


class Province(models.Model):
    """
    省份
    """
    name = models.CharField(u'名称', max_length=200, blank=True)
    chart = models.CharField(u'url标志', max_length=200, blank=True)
    ename = models.CharField(u'英文简称', max_length=200, blank=True)
    country = models.ForeignKey(Country)
    status = models.BooleanField(u"启用", default=False)
    latitude = models.FloatField(u'经度', max_length=100, default=0.0)
    longitude = models.FloatField(u'纬度', max_length=100, default=0.0)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = verbose_name = u"省份"

    def __unicode__(self):
        return u'%s' % self.name

    # def get_absolute_url(self):
    #     return reverse('country_index', kwargs={'country_chart': self.chart})


class City(models.Model):
    """
    城市
    """
    name = models.CharField(u'名称', max_length=200, blank=True)
    chart = models.CharField(u'url标志', max_length=200, blank=True,null=True)
    ename = models.CharField(u'英文简称', max_length=200, blank=True,null=True)
    code = models.CharField(u'编码', max_length=200, blank=True, null=True)
    province = models.ForeignKey(Province)
    country = models.ForeignKey(Country)
    airport = models.CharField(u'航空', max_length=200, blank=True,null=True)
    status = models.BooleanField(u"启用", default=False)
    latitude = models.FloatField(u'经度', max_length=100, default=0.0)
    longitude = models.FloatField(u'纬度', max_length=100, default=0.0)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = verbose_name = u"城市"

    def __unicode__(self):
        return u'%s' % self.name

    # def get_absolute_url(self):
    #     return reverse('country_city_index', kwargs={'city_chart': self.chart})


class Location(models.Model):
    """
    行政区
    """
    name = models.CharField(u'名称', max_length=200, blank=True)
    chart = models.CharField(u'url标志', max_length=200, blank=True, null=True)
    ename = models.CharField(u'英文简称', max_length=200, blank=True, null=True)
    city = models.ForeignKey(City)
    status = models.BooleanField(u"启用", default=False)
    latitude = models.FloatField(u'经度', max_length=100, default=0.0)
    longitude = models.FloatField(u'纬度', max_length=100, default=0.0)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = verbose_name = u"行政区"

    def __unicode__(self):
        return u'%s' % self.name

    # def get_absolute_url(self):
    #     return reverse('country_location_index', kwargs={'city_chart': self.city.chart, 'location_chart': self.chart})


class Zone(models.Model):
    """
    商业区
    """
    name = models.CharField(u'名称', max_length=200)
    chart = models.CharField(u'url标志', max_length=200, blank=True, null=True)
    ename = models.CharField(u'英文简称', max_length=200, blank=True, null=True)
    city = models.ForeignKey(City, verbose_name=u"城市", blank=True, null=True, db_constraint=False)
    status = models.BooleanField(u"启用", default=False)
    latitude = models.FloatField(u'经度', max_length=100, default=0.0)
    longitude = models.FloatField(u'纬度', max_length=100, default=0.0)
    desc = models.TextField(u"简介", blank=True, null=True)
    mapuse = models.CharField(u"地图使用", max_length=2)
    mappic = models.CharField(u"地图图片", max_length=40, blank=True, null=True)
    range = models.CharField(u"Range", max_length=200, blank=True, null=True)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = verbose_name = u"商业区"

    def __unicode__(self):
        return u'%s' % self.name

    # def get_absolute_url(self):
    #     return reverse('country_zone_index',
    #                    kwargs={'city_chart': self.location.city.chart, 'location_chart': self.location.chart,
    #                            'zone_chart': self.chart})