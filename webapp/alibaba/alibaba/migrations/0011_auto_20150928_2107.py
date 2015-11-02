# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alibaba', '0010_auto_20150928_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zone',
            name='city',
            field=models.ForeignKey(db_constraint=False, verbose_name='\u57ce\u5e02', blank=True, to='alibaba.City', null=True),
        ),
    ]
