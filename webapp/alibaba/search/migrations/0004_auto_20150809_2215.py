# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_category_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, verbose_name='\u5206\u7c7b\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='link',
            name='name',
            field=models.CharField(max_length=200, verbose_name='\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, verbose_name='\u540d\u79f0'),
        ),
    ]
