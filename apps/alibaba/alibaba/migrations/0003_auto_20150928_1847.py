# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('alibaba', '0002_auto_20150928_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zone',
            name='desc',
            field=models.TextField(null=True, verbose_name='\u7b80\u4ecb', blank=True),
        ),
    ]
