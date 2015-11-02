# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alibaba', '0007_auto_20150928_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zone',
            name='range',
            field=models.CharField(max_length=200, null=True, verbose_name='Range', blank=True),
        ),
    ]
