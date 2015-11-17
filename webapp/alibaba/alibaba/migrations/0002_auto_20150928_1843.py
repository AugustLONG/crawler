# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
	dependencies = [
		('alibaba', '0001_initial'),
	]

	operations = [
		migrations.AlterField(
			model_name='city',
			name='airport',
			field=models.CharField(max_length=200, null=True, verbose_name='\u822a\u7a7a', blank=True),
		),
	]
