# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
	dependencies = [
		('alibaba', '0006_auto_20150928_2031'),
	]

	operations = [
		migrations.RenameField(
			model_name='zone',
			old_name='city',
			new_name='city_id',
		),
	]
