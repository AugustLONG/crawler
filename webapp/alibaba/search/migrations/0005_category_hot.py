# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
	dependencies = [
		('search', '0004_auto_20150809_2215'),
	]

	operations = [
		migrations.AddField(
			model_name='category',
			name='hot',
			field=models.SmallIntegerField(default=0, verbose_name='\u70ed\u95e8'),
		),
	]
