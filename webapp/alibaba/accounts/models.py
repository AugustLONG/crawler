#coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from userena.models import UserenaLanguageBaseProfile
from userena.utils import user_model_label
from django.contrib.auth.models import User
import datetime

class Profile(UserenaLanguageBaseProfile):
    """ Default profile """
    GENDER_CHOICES = (
        (1, _('Male')),
        (2, _('Female')),
    )

    user = models.OneToOneField(user_model_label,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')

    gender = models.PositiveSmallIntegerField(_('gender'),
                                              choices=GENDER_CHOICES,
                                              blank=True,
                                              null=True)
    website = models.URLField(_('website'), blank=True)
    location =  models.CharField(_('location'), max_length=255, blank=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    about_me = models.TextField(_('about me'), blank=True)

    @property
    def age(self):
        if not self.birth_date:
            return False
        else:
            today = datetime.date.today()
            # Raised when birth date is February 29 and the current year is not a
            # leap year.
            try:
                birthday = self.birth_date.replace(year=today.year)
            except ValueError:
                day = today.day - 1 if today.day != 1 else today.day + 2
                birthday = self.birth_date.replace(year=today.year, day=day)
            if birthday > today:
                return today.year - self.birth_date.year - 1
            else:
                return today.year - self.birth_date.year

from scraper.models import Website
class UserWebSite(models.Model):
    name = models.CharField(u"名称", max_length=255)
    tag = models.CharField(u"标签", max_length=255, blank=True)
    website = models.ForeignKey(Website)
    user = models.ForeignKey(User)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"用户收藏的网站"
        get_latest_by = "created"


class UserNoteBook(models.Model):
    name = models.CharField(u"笔记名称", max_length=255)
    parent = models.ForeignKey("self", blank=True)
    order = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = verbose_name = u"用户笔记本"
        get_latest_by = "created"


class UserNote(models.Model):
    name = models.CharField(u"笔记名称", max_length=255)
    tag = models.CharField(u"笔记标签", max_length=255, blank=True)
    note = models.TextField(u"笔记内容")
    order = models.IntegerField(default=0)
    notebook = models.ForeignKey(UserNoteBook, verbose_name=u"笔记本")
    website = models.ForeignKey(Website)
    user = models.ForeignKey(User)
    created = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    updated = models.DateTimeField(u"更新时间", auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u"用户笔记"
        get_latest_by = "created"



