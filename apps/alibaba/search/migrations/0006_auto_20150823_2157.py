# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('search', '0005_category_hot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='tags',
            field=models.ManyToManyField(to='search.Tag', blank=True),
        ),
    ]
