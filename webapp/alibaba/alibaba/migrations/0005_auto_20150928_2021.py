# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alibaba', '0004_auto_20150928_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='chart',
            field=models.CharField(max_length=200, null=True, verbose_name='url\u6807\u5fd7', blank=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='ename',
            field=models.CharField(max_length=200, null=True, verbose_name='\u82f1\u6587\u7b80\u79f0', blank=True),
        ),
    ]
