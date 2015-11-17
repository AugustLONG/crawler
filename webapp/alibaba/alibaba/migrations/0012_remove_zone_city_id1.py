# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
	dependencies = [
		('alibaba', '0011_auto_20150928_2107'),
	]

	operations = [
		migrations.RemoveField(
			model_name='zone',
			name='city_id1',
		),
	]
