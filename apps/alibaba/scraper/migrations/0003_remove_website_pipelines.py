# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('scraper', '0002_auto_20150911_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='website',
            name='pipelines',
        ),
    ]
