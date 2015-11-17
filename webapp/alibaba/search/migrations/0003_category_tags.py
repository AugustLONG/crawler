# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('search', '0002_auto_20150809_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='tags',
            field=models.ManyToManyField(to='search.Tag', null=True, blank=True),
        ),
    ]
