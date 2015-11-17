# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
	dependencies = [
		('search', '0001_initial'),
	]

	operations = [
		migrations.CreateModel(
			name='Tag',
			fields=[
				('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
				('name', models.CharField(max_length=10, verbose_name='\u540d\u79f0')),
				('slug', models.SlugField(unique=True, max_length=100, verbose_name='\u522b\u540d')),
				('enabled', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
				('hot', models.SmallIntegerField(default=0, verbose_name='\u70ed\u5ea6')),
				('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
				('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
			],
			options={
				'ordering': ('hot',),
				'get_latest_by': 'created',
				'verbose_name': '\u641c\u7d22\u6807\u7b7e',
				'verbose_name_plural': '\u641c\u7d22\u6807\u7b7e',
			},
		),
		migrations.AlterField(
			model_name='link',
			name='name',
			field=models.CharField(max_length=10, verbose_name='\u540d\u79f0'),
		),
		migrations.AlterField(
			model_name='link',
			name='url',
			field=models.URLField(verbose_name='\u5730\u5740'),
		),
	]
