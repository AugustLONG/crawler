# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
	dependencies = [
		('search', '0007_pagemodule'),
	]

	operations = [
		migrations.RemoveField(
			model_name='pagemodule',
			name='website',
		),
	]
