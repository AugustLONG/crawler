# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
	dependencies = [
		('search', '0010_auto_20150914_0225'),
	]

	operations = [
		migrations.AddField(
			model_name='categoryforms',
			name='analyzerable',
			field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5206\u8bcd'),
		),
		migrations.AddField(
			model_name='categoryforms',
			name='indexable',
			field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u7d22\u5f15'),
		),
		migrations.AddField(
			model_name='categoryforms',
			name='searchable',
			field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u641c\u7d22'),
		),
	]
