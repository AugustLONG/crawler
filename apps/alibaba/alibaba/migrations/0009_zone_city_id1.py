# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('alibaba', '0008_auto_20150928_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='zone',
            name='city_id1',
            field=models.IntegerField(default=0, verbose_name='\u57ce\u5e02'),
        ),
    ]
