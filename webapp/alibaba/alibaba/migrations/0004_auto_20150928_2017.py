# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alibaba', '0003_auto_20150928_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='code',
            field=models.CharField(max_length=200, null=True, verbose_name='\u7f16\u7801', blank=True),
        ),
    ]
