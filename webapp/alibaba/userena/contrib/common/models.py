# coding=utf-8
import datetime
from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name="favorite_user")
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"用户收藏"
        get_latest_by = "created"


class Vote(models.Model):
    user = models.ForeignKey(User, related_name="vote_user")
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"用户点赞"
        get_latest_by = "created"

class SearchRecord(models.Model):
    word = models.CharField(u"搜素词", max_length=255, db_index=True)
    user = models.ForeignKey(User, related_name="search_user")
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"用户搜索关键词"
        get_latest_by = "created"
