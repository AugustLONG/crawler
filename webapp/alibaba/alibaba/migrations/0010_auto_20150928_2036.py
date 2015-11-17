# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('alibaba', '0009_zone_city_id1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zone',
            name='city_id',
        ),
        migrations.AddField(
            model_name='zone',
            name='city',
            field=models.ForeignKey(verbose_name='\u57ce\u5e02', blank=True, to='alibaba.City', null=True),
        ),
    ]
